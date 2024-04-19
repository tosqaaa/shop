from django.contrib import admin

from .models import ShippingAddress, Order, OrderItem

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'address', 'email', 'zip_code', 'country']
    fields = ['user', 'city', 'address', 'email', 'zip_code', 'country']
    search_fields = ['user__username', 'city', 'address', 'email', 'zip_code', 'country']
    list_filter = ['user']
    
    
    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'
        ordering = ['user']
        
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'created', 'updated', 'paid', 'discount']
    fields = ['user', 'shipping_address', 'amount', 'created', 'updated', 'paid', 'discount']
    search_fields = ['user__username', 'amount', 'created', 'updated', 'paid', 'discount']
    list_filter = ['user', 'created', 'updated', 'paid']
    readonly_fields = ['created', 'updated']
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']
        
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity', 'user']
    fields = ['order', 'product', 'price', 'quantity', 'user']
    search_fields = ['order', 'product', 'price', 'quantity', 'user']
    list_filter = ['order', 'product', 'price', 'quantity', 'user']
    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
        ordering = ['order']
