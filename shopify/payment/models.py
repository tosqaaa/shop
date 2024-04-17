from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from shop.models import Product
from django.urls import reverse

User = get_user_model()

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,verbose_name='Пользователь')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    email = models.EmailField(verbose_name='Электронная почта')
    zip_code = models.CharField(max_length=100, verbose_name='Индекс')
    country = models.CharField(max_length=100, verbose_name='Страна')

    def __str__(self) -> str:
        return f'Shipping adress for {self.user.username}, id={self.id}'
    
    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'
        ordering = ['user']
        
        
class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Адрес доставки')
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],verbose_name='Скидка')
        
        
    def __str__(self) -> str:
        return f'Order {self.id}'
    
    def get_absolute_url(self):
        return reverse("shop:order_detail", kwargs={"pk": self.pk})
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    
    def __str__(self) -> str:
        return f'OrderItem {self.id}'
    
    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
        ordering = ['order']
    
    