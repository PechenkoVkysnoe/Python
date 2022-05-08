from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import  ContentType

User = get_user_model()


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category Name')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Product Name')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image')
    description = models.TextField(verbose_name='Description', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.title


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Customer Name', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart name', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Product Name', on_delete=models.CASCADE)
    quality = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='General Price')

    def __str__(self):
        return f'Cart product {self.product.title}'


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name="Cart's owner", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True)
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='General Price')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Customer', on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, verbose_name='Phone number')
    address = models.CharField(max_length=255, verbose_name=' Address')

    def __str__(self):
        return f'Customer: {self.user.first_name} {self.user.last_name}'


class Specification(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField
    name = models.CharField(max_length=255, verbose_name='Product name for specification')

    def __str__(self):
        return f"Product's specification {self.name}"
