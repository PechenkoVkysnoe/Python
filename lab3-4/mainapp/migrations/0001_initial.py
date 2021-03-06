# Generated by Django 4.0.4 on 2022-05-22 17:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_order', models.BooleanField(default=False)),
                ('for_anonymous_user', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Category Name')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Short',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Product Name')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Image')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Price')),
                ('size', models.CharField(max_length=255, verbose_name='Размер')),
                ('compound', models.CharField(max_length=255, verbose_name='Состав')),
                ('origin_country', models.CharField(max_length=255, verbose_name='Страна производства')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Імя')),
                ('second_name', models.CharField(max_length=255, verbose_name='Прозвішча')),
                ('third_name', models.CharField(max_length=255, verbose_name='Імя па бацьку')),
                ('phone', models.CharField(default='', max_length=20, verbose_name='Тэлефон')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрас')),
                ('status', models.CharField(choices=[('new', 'Новая замова'), ('in_progress', 'Замова ў апрацоўцы'), ('is_ready', 'Замова гатовы'), ('completed', 'Замова выкананы')], default='new', max_length=255, verbose_name='Статус замовы')),
                ('buying_type', models.CharField(choices=[('self', 'Самавываз'), ('delivery', 'Дастаўка')], default='self', max_length=255, verbose_name='Тып замовы')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Каментарый да заказу')),
                ('order_data', models.DateField(default=datetime.datetime(2022, 5, 22, 17, 46, 54, 617776, tzinfo=utc), verbose_name='Дата атрымання замовы')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cart', verbose_name='Кошык')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_orders', to='mainapp.customer', verbose_name='Пакупнік')),
            ],
        ),
        migrations.CreateModel(
            name='LongShort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Product Name')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Image')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Price')),
                ('size', models.CharField(max_length=255, verbose_name='Размер')),
                ('compound', models.CharField(max_length=255, verbose_name='Состав')),
                ('belt_length', models.CharField(default=0, max_length=255, verbose_name='Длина пояса')),
                ('origin_country', models.CharField(max_length=255, verbose_name='Страна производства')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Product Name')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Image')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Price')),
                ('size', models.CharField(max_length=255, verbose_name='Размер')),
                ('compound', models.CharField(max_length=255, verbose_name='Состав')),
                ('length', models.CharField(max_length=255, verbose_name='Длина')),
                ('origin_country', models.CharField(max_length=255, verbose_name='Страна производства')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('quality', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='mainapp.cart', verbose_name='Cart name')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.customer', verbose_name='Customer Name')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.customer', verbose_name="Cart's owner"),
        ),
    ]
