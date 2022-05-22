from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from .models import Category, Cart, Customer, Short, Dress, LongShort

#По факту нужен для того, чтоыб на каждой странице добавлять девый бар
#этот миксин работает и для категорий и для товаров
class CategoryDetailMixin(SingleObjectMixin):

    CATEGORY_SLUG_TO_PRODUCT_MODEL = {
        'shorts': Short,
        'dresses': Dress,
        'longshorts': LongShort
    }

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            #Получаем модель, чтобы отобразить, какие товары в ней присутствуют
            model = self.CATEGORY_SLUG_TO_PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.object.get_categories_for_left_sidebar()
            #по факту это получается queryset из моделей, которые у нас есть
            context['category_products'] = model.objects.all()

        else:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.object.get_categories_for_left_sidebar()

        return context


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()

            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )

            cart = Cart.objects.filter(owner=customer, in_order=False).first()

            if not cart:
                cart = Cart.objects.create(owner=customer)

        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()

            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)

        self.cart = cart

        return super().dispatch(request, *args, **kwargs)
