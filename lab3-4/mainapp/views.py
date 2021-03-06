from django.db import transaction
from django.shortcuts import render
# Экземпляры ContentTypeпредставляют и хранят информацию о моделях, установленных в вашем проекте
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, View
from django.http import HttpResponseRedirect
from .models import (
    Category,
    CartProduct,
    Short,
    Dress,
    LongShort
)
from .managers import LatestProducts
from . import tasks
from .mixins import (
    CategoryDetailMixin,
    CartMixin
)
from .forms import OrderForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import logging


# Create your views here.
'''По факту, вся логика
request-запрос, который даёт пользователь на сервер джанго'''
'''Если выполнен url запрос по данному адресу, то выполнится метод get'''

logger = logging.getLogger('main')


class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        logger.info("BaseView")
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page('short', 'dress', 'longshort',
                                                                     with_respect_to='short')
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart
        }

        return render(request, 'base.html', context)


# при помощи одного этого представления, мы можем выводить информацию сразу же из нескольких моделей
# то есть нам не надо писать отдельные url pattern для того, чтобы выводить объекты разных моделей
# мы на уровне dispatch сразу определяем, что это за модель и выводим информацию о данном объекте
class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        'short': Short,
        'dress': Dress,
        'longshort': LongShort
    }

    def dispatch(self, request, *args, **kwargs):
        logger.info("ProductDetailView")
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()

        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart

        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    # добавление дополнительной информации
    # Контекст который я хочу вывести в моеё вьюшке(аналогия с функцией)
    # Возвращает словарь, представляющий контекст шаблона. Предоставленные аргументы ключевого слова будут составлять возвращаемый контекст.
    def get_context_data(self, **kwargs):
        logger.info("CategoryDetailView")
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart

        return context


class AddToCartView(LoginRequiredMixin, CartMixin, View):

    def get(self, request, *args, **kwargs):
        logger.info("AddToCartView")  # pragma: no cover
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        # content_type Тип содержимого, используемый для ответа.
        content_type = ContentType.objects.get(model=ct_model)
        # ContentType.model_class() Возвращает класс модели, представленный этим ContentType экземпляром.
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )

        if created:
            self.cart.products.add(cart_product)

        '''HttpResponseRedirect означает, что ответ будет перенаправлять нас куда-то'''
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(LoginRequiredMixin, CartMixin, View):

    def get(self, request, *args, **kwargs):
        logger.info("DeleteFromCartView")
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        cart_product.delete()

        return HttpResponseRedirect('/cart/')


class CartView(LoginRequiredMixin, CartMixin, View):

    def get(self, request, *args, **kwargs):
        logger.info("CartView")
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories
        }

        return render(request, 'cart.html', context)


#
class ChangeQTYView(LoginRequiredMixin, CartMixin, View):

    def post(self, request, *args, **kwargs):
        logger.info("ChangeQTYView")
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        # if request.POST.get('quality')
        
        try:
            quality = int(request.POST.get('quality'))
        except:
            quality = 0
        cart_product.quality = quality
        cart_product.save()

        return HttpResponseRedirect('/cart/')


class CheckoutView(LoginRequiredMixin, CartMixin, View):

    def get(self, request, *args, **kwargs):
        logger.info("CheckoutView")
        categories = Category.objects.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }

        return render(request, 'checkout.html', context)

class CabinetView(View):

    def get(self, request, *args, **kwargs):
        logger.info("CheckoutView")
        categories = Category.objects.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }

        return render(request, 'checkout.html', context)

class MakeOrderView(LoginRequiredMixin, CartMixin, View):

    # декоратор нужен для того, чтобы при ошибке все откатилось
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        logger.info("MakeOrderView")
        form = OrderForm(request.POST or None)
        customer = request.user.customer

        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.second_name = form.cleaned_data['second_name']
            new_order.third_name = form.cleaned_data['third_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_data']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            tasks.make_order.delay(
                new_order.first_name,
                new_order.second_name,
                new_order.third_name,
                new_order.phone,
                new_order.address,
                new_order.buying_type,
                new_order.order_date,
                new_order.comment
            )
            messages.add_message(request, messages.INFO, 'Дзякуй, за замову! Мэнэджар з Вамі звяжацца')

            return HttpResponseRedirect('/')
        messages.add_message(request, messages.INFO, 'Калі ласка, увядзіце правільны фармат даты і нумара.\nПрыклад дакладнага фармату\n+375292868321 2022-05-29')
        return HttpResponseRedirect('/checkout/')
