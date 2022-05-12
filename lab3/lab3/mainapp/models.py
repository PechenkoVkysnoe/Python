from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, view_name):
    ct_model = obj.__class__._meta.model_name
    return reverse(view_name, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:
    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)

        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),
                                  reverse=True)
        return products


class LatestProducts:
    objects = LatestProductsManager()


class CategoryManager(models.Manager):
    CATEGORY_NAME_COUNT_NAME = {
        'Notebook': 'notebook__count',
        'Smartphone': 'smartphone__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('notebook', 'smartphone')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category Name')
    slug = models.SlugField(unique=True)
    object = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
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

    def get_model_name(self):
        return self.__class__.__name__.lower()


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Customer Name', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart name', on_delete=models.CASCADE, related_name='related_product')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quality = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='General Price')

    def __str__(self):
        # return f'Cart product {self.content_object.title}'
        return "Продукт: {} (для корзины)".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.quality * self.content_object.price
        super().save(*args, **kwargs)


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
    user = models.ForeignKey(User, verbose_name='Customer', related_name='related_orders', on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, verbose_name='Phone number', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name=' Address', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_customer')
    def __str__(self):
        return f'Customer: {self.user.first_name} {self.user.last_name}'


class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Diagonal')
    display_type = models.CharField(max_length=255, verbose_name="Display's type")
    processor_frequency = models.CharField(max_length=255, verbose_name="Processor's frequency")
    ram = models.CharField(max_length=255, verbose_name='Ram')
    time_without_charge = models.CharField(max_length=255, verbose_name='Battery life')
    video = models.CharField(max_length=255, verbose_name='Video card')

    def __str__(self):
        return f"{self.category.name}: {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Diagonal')
    display_type = models.CharField(max_length=255, verbose_name="Display's type")
    resolution = models.CharField(max_length=255, verbose_name="Windows's resolution")
    ram = models.CharField(max_length=255, verbose_name='Ram')
    time_without_charge = models.CharField(max_length=255, verbose_name='Battery life')
    sd = models.BooleanField(default=True, verbose_name='Наличие SD карты')
    sd_volume_max = models.CharField(max_length=255, null=True, blank=True, verbose_name="Maximum value of sd card")
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Mp of frontal camera')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Mp of main camera')

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
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен'),
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    second_name = models.CharField(max_length=255, verbose_name='Фамилия')
    third_name = models.CharField(max_length=255, verbose_name='Отчество')
    phone = models.CharField(max_length=20, verbose_name='Телефон', default='')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(max_length=255, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)

    buying_type = models.CharField(
        max_length=255,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_ad = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_data = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)
