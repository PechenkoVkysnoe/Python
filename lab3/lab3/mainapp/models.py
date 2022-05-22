from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.urls import reverse
from django.utils import timezone


## вывод продуктов на главной странице
class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)

        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:2]
            products.extend(model_products)

        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)

            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),
                                  reverse=True)

        return products


#
class LatestProducts:
    objects = LatestProductsManager()


# По факту мы сейчас говорим, что мы хотим использовать того юзера, который у нас прописан в settings.AUTH_USER_MODEL(Настройка скрытая, но она есть)
User = get_user_model()


# считаетколичество каждой модели(необходимо для левого бара)
def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


#
# функция, которая позволяет не писать для каждого продукта функцию для нахождения конечного endpointa(url)
def get_product_url(obj, view_name):
    ct_model = obj.__class__._meta.model_name

    return reverse(view_name, kwargs={'ct_model': ct_model, 'slug': obj.slug})


#
class CategoryManager(models.Manager):
    CATEGORY_NAME_COUNT_NAME = {
        'Сукенка': 'dress__count',
        'Кашуля': 'short__count',
        'Рубаха': 'longshort__count'
    }

    '''def get_queryset(self):
        return super().get_queryset()'''

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('dress', 'short', 'longshort')
        # Получаем
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]

        return data


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category Name')
    # slug-уникальный фрагмент url адреса аассоциированный с конкретной записью
    slug = models.SlugField(unique=True)
    #
    object = CategoryManager()

    def __str__(self):
        return self.name

    # метод, который формирует нужный нам маршрут(в html), маршрут к конкретной записи
    def get_absolute_url(self):
        #
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    # Вроде класс для админ панели/создать для неё миграцию я не смогу
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Product Name')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image')
    description = models.TextField(verbose_name='Description', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.title

    #
    def get_model_name(self):
        return self.__class__.__name__.lower()


# Промежуточный продукт, который относится только к корзине
class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Customer Name', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart name', on_delete=models.CASCADE, related_name='related_product')
    # Даёт понимаение того, какой именно продукт сейчас у меня
    # Content_type-микро фремформ, который выдит все мои модели, которые есть у меня в install_apps и соответсвенно
    # когда я зайду в админку и увижу все модели, которые есть у меня в проекте
    # оторое позволяет отслеживать все модели вашего Django проекта. Это приложение предоставляет высокоуровневый,
    # обобщенный интерфейс для работы с вашими моделями.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # индификатор instanse этой модели
    object_id = models.PositiveIntegerField()
    # content_object к примеру, чтобы создать cartProduct и поместить туда content_object
    # нам во первых надо взят ькакой-нибудь продукт(p=ShortProduct.objects.get(pk=1)
    # CartProduct.objects.create(content_object=p) и вот как только я это сделаю, у меня content_type и object_id заполнятся автоматически
    # и вот таким образом у меня создаются cartProduct, то есть у меня есть 3 cartProduct, но все относятся к разным моделям и при этом они используются в одной таблице
    # cartProduct  с одним внешним ключом
    content_object = GenericForeignKey('content_type', 'object_id')
    quality = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='General Price')

    def __str__(self):
        return f'Cart product {self.content_object.title}'

    # Отрабатывает при создании нового cartProduct
    def save(self, *args, **kwargs):
        self.final_price = self.quality * self.content_object.price
        super().save(*args, **kwargs)


# related_product/related_cart нужен для того, что бы разрешить проблемы того, что card ссылается на cardProduct и наоборот
# Если мы напишем cartproduct.related_card мы узнаем к какой корзине относится
class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name="Cart's owner", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='relate_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='General Price')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    #
    user = models.ForeignKey(User, verbose_name='Customer', related_name='related_orders', on_delete=models.CASCADE)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_customer',
                                    blank=True, null=True)

    def __str__(self):
        return f'Customer: {self.user.first_name} {self.user.last_name}'


class Short(Product):
    size = models.CharField(max_length=255, verbose_name='Размер')
    compound = models.CharField(max_length=255, verbose_name='Состав')
    origin_country = models.CharField(max_length=255, verbose_name='Страна производства')

    def __str__(self):
        return f"{self.category.name}: {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Dress(Product):
    size = models.CharField(max_length=255, verbose_name='Размер')
    compound = models.CharField(max_length=255, verbose_name='Состав')
    length = models.CharField(max_length=255, verbose_name='Длина')
    origin_country = models.CharField(max_length=255, verbose_name='Страна производства')

    def __str__(self):
        return f"{self.category.name}: {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class LongShort(Product):
    size = models.CharField(max_length=255, verbose_name='Размер')
    compound = models.CharField(max_length=255, verbose_name='Состав')
    belt_length = models.CharField(max_length=255, verbose_name='Длина пояса', default=0)
    origin_country = models.CharField(max_length=255, verbose_name='Страна производства')

    def __str__(self):
        return f"{self.category.name}: {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'
    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'
    STATUS_CHOICES = (
        (STATUS_NEW, 'Новая замова'),
        (STATUS_IN_PROGRESS, 'Замова ў апрацоўцы'),
        (STATUS_READY, 'Замова гатовы'),
        (STATUS_COMPLETED, 'Замова выкананы'),
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самавываз'),
        (BUYING_TYPE_DELIVERY, 'Дастаўка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Пакупнік', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Імя')
    second_name = models.CharField(max_length=255, verbose_name='Прозвішча')
    third_name = models.CharField(max_length=255, verbose_name='Імя па бацьку')
    phone = models.CharField(max_length=20, verbose_name='Тэлефон', default='')
    #
    cart = models.ForeignKey(Cart, verbose_name='Кошык', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрас', null=True, blank=True)
    status = models.CharField(max_length=255, verbose_name='Статус замовы', choices=STATUS_CHOICES, default=STATUS_NEW)

    buying_type = models.CharField(
        max_length=255,
        verbose_name='Тып замовы',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Каментарый да заказу', null=True, blank=True)
    order_data = models.DateField(verbose_name='Дата атрымання замовы', default=timezone.now)

    def __str__(self):
        return str(self.id)
