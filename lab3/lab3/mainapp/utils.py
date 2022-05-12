from django.db import models


def recalc_cart(cart):
    card_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if card_data['final_price__sum']:
        cart.final_price = card_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.total_products = card_data['id__count']
    cart.save()
