from django.urls import path
from .views import products_view, product_detail_view, product_category_view

app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('products/<slug:slug>', product_detail_view, name='product_detail'),
    path('products/category/<slug:slug>',
         product_category_view, name='product_category'),
]
