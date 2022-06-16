import logging
from decimal import Decimal
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse


from .models import (
    Category,
    LongShort,
    CartProduct, 
    Cart,
    Order
)

from django.test import Client

User = get_user_model()
logging.disable()


class BasePageTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password="password")
        self.client = Client(enforce_csrf_checks=False)
        self.client.force_login(self.user)

        self.category = Category.objects.create(name='Рубаха', slug='longshorts')
        self.longshort = LongShort.objects.create(
            category=self.category,
            title="Test",
            slug="test-slug",
            image='/media/longshort1.jpg',
            size='160',
            compound = '100%',
            belt_length = '30',
            origin_country = 'RB',
            description="Test description",
            price=Decimal("100.0"),
        )
        self.cart = Cart.objects.create(owner=self.user.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.user.customer,
            cart=self.cart,
            content_object=self.longshort
        )

    def test_cart_final_price(self):
        self.assertEqual(self.cart.final_price, Decimal("100.0"))

    def test_base_page_status_code(self):
        response = self.client.get(reverse('base'))
        self.assertEqual(response.status_code, 200)

    def test_make_order_view_success(self):
        data = {
            'first_name': 'Vladislav',
            'second_name': 'Pliska',
            'third_name': 'Sergeevich',
            'phone': 12321123,
            'address':'asdfasdf',
            'buying_type': Order.BUYING_TYPE_DELIVERY,
            'order_data': '2022-05-28',
            'comment': 'asdfasdf'
        }
        response = self.client.post(reverse('make_order'), data)
        self.assertEqual(Order.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
    

    def test_make_order_view_failure(self):
        data = {
            'first_name': 'Vladislav',
            'second_name': 'Pliska',
            'third_name': 'Sergeevich',
            'address':'asdfasdf',
            'buying_type': Order.BUYING_TYPE_DELIVERY,
            'order_data': '22.05.2022',
            'comment': 'asdfasdf'
        }
        response = self.client.post(reverse('make_order'), data)
        self.assertEqual(Order.objects.all().count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/checkout/')



