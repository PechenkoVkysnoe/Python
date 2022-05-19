from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe
from .models import *
from PIL import Image

# AXTUNG!!!!!!
# Register your models here.
'''Тут регистрируются модели, для того, чтобы они находились в админке'''


'''class NotebookAdminForm(ModelForm):
    MIN_RESOLUTION = (200, 200)
    MAX_RESOLUTION = (10000, 10000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = \
            f'<span style="color:red">Загружайте изображение с минимальным разширением {self.MIN_RESOLUTION[0]}x{self.MIN_RESOLUTION[1]} \n ' \
            f'Загружайте изображение с максимальным разширением {self.MAX_RESOLUTION[0]}x{self.MAX_RESOLUTION[1]}</span>'

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        if img.height < self.MIN_RESOLUTION[0] or img.width < self.MIN_RESOLUTION[1]:
            raise ValidationError('Загруженное изображение меньше допустимого размера')
        if img.height > self.MAX_RESOLUTION[0] or img.width > self.MAX_RESOLUTION[1]:
            raise ValidationError('Загруженное изображение больше допустимого размера')
        return image'''

#Для того, чтобы у рубашки была категория только рубашка
class ShortAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.object.filter(slug='shorts'))

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DressAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.object.filter(slug='dresses'))

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class LongShortAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.object.filter(slug='longshorts'))

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Short, ShortAdmin)
admin.site.register(Dress, DressAdmin)
admin.site.register(LongShort, LongShortAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
