# Generated by Django 4.0.4 on 2022-05-09 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Smartphone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Product Name')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Price')),
                ('diagonal', models.CharField(max_length=255, verbose_name='Diagonal')),
                ('display_type', models.CharField(max_length=255, verbose_name="Display's type")),
                ('resolution', models.CharField(max_length=255, verbose_name="Windows's resolution")),
                ('ram', models.CharField(max_length=255, verbose_name='Ram')),
                ('time_without_charge', models.CharField(max_length=255, verbose_name='Battery life')),
                ('sd', models.BooleanField(default=True)),
                ('sd_volume_max', models.CharField(max_length=255, verbose_name='Maximum value of sd card')),
                ('frontal_cam_mp', models.CharField(max_length=255, verbose_name='Mp of frontal camera')),
                ('main_cam_mp', models.CharField(max_length=255, verbose_name='Mp of main camera')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Product Name')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Price')),
                ('diagonal', models.CharField(max_length=255, verbose_name='Diagonal')),
                ('display_type', models.CharField(max_length=255, verbose_name="Display's type")),
                ('processor_frequency', models.CharField(max_length=255, verbose_name="Processor's frequency")),
                ('ram', models.CharField(max_length=255, verbose_name='Ram')),
                ('time_without_charge', models.CharField(max_length=255, verbose_name='Battery life')),
                ('video', models.CharField(max_length=255, verbose_name='Video card')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]