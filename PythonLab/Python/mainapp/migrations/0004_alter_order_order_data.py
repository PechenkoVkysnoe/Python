# Generated by Django 3.2.13 on 2022-05-31 19:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_order_order_data_alter_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_data',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата атрымання замовы'),
        ),
    ]
