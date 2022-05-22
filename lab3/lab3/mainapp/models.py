from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from .managers import CategoryManager


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category Name')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    # метод, который формирует нужный нам маршрут(в html), маршрут к конкретной записи
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Product Name')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image', blank=True)
    description = models.TextField(verbose_name='Description', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    #для контенттайпа
    def get_model_name(self):
        return self.__class__.__name__.lower()
    #для конкретного продукта юрл его категории
    def get_product_url(self, view_name):
        ct_model = self.__class__._meta.model_name

        return reverse(view_name, kwargs={'ct_model': ct_model, 'slug': self.slug})


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Customer Name', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart name', on_delete=models.CASCADE, related_name='products')
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    quality = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'Cart product {self.content_object.title}'

    @property
    def final_price(self):
        return self.quality * self.content_object.price


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name="Cart's owner", on_delete=models.CASCADE)
    total_products = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def final_price(self):
        s = 0
        for item in self.products.all():
            s += item.final_price
        return s

    @property
    def total_products(self):
        return self.products.all().count()

class Customer(models.Model):
    '''
        Customer model
    '''
    user = models.OneToOneField(User, verbose_name='Customer', related_name='customer', on_delete=models.CASCADE)

    def __str__(self):
        return f'Customer: {self.user.first_name} "{self.user.username}" {self.user.last_name}'

# джанга
@receiver(post_save, sender=User)
def update_user_customer(instance, created, **kwargs):
    '''
        Create Customer model when User model creating
    '''

    if created:
        Customer.objects.create(user=instance)
    instance.customer.save()


class Short(Product):
    size = models.CharField(max_length=255, verbose_name='Размер')
    compound = models.CharField(max_length=255, verbose_name='Состав')
    origin_country = models.CharField(max_length=255, verbose_name='Страна производства')

    def __str__(self):
        return f"{self.category.name}: {self.title}"

    def get_absolute_url(self):
        return self.get_product_url('product_detail')


class Dress(Product):
    size = models.CharField(max_length=255, verbose_name='Размер')
    compound = models.CharField(max_length=255, verbose_name='Состав')
    length = models.CharField(max_length=255, verbose_name='Длина')
    origin_country = models.CharField(max_length=255, verbose_name='Страна производства')

    def __str__(self):
        return f"{self.category.name}: {self.title}"

    def get_absolute_url(self):
        return self.get_product_url('product_detail')


class LongShort(Product):
    size = models.CharField(max_length=255, verbose_name='Размер')
    compound = models.CharField(max_length=255, verbose_name='Состав')
    belt_length = models.CharField(max_length=255, verbose_name='Длина пояса', default=0)
    origin_country = models.CharField(max_length=255, verbose_name='Страна производства')

    def __str__(self):
        return f"{self.category.name}: {self.title}"

    def get_absolute_url(self):
        return self.get_product_url('product_detail')


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

    customer = models.ForeignKey(Customer, verbose_name='Пакупнік', related_name='customer_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Імя')
    second_name = models.CharField(max_length=255, verbose_name='Прозвішча')
    third_name = models.CharField(max_length=255, verbose_name='Імя па бацьку')
    phone = models.CharField(max_length=20, verbose_name='Тэлефон', default='')
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
    order_data = models.DateField(verbose_name='Дата атрымання замовы', default=timezone.now())

    def __str__(self):
        return f'{self.id}'
