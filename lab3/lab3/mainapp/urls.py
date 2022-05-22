from django.template.defaulttags import url

from mainapp.views import (
    BaseView, 
    ProductDetailView, 
    CategoryDetailView, 
    CartView, 
    AddToCartView, 
    DeleteFromCartView, 
    ChangeQTYView, 
    CheckoutView, 
    MakeOrderView
)
from django.urls import path

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    #path('products/<str:ct_model>/<slug:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    #url(r'^products/<str:ct_model>/(?P<pk>\d+)/$', ProductDetailView.as_view()),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-quality/<str:ct_model>/<str:slug>/', ChangeQTYView.as_view(), name='change_quality'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
]
# тут не регулярное выражение, потому что нам отдуда нечего брать, для того, чтобы находить нужные нам объекты, потому что все что нам  нужно бы забираем из request, то есть сразу находим пользователя, а через пользователя находим корзину и её render
