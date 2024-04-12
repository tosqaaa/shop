from django.urls import path
from .views import cart_view, cart_add

app_name = 'cart'
urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('add/', cart_add, name='cart_add')
]
