from django.contrib import admin
from django.forms import ModelChoiceField
from .models import Short, LongShort, Category, Dress, Cart, Order, Customer, CartProduct


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
