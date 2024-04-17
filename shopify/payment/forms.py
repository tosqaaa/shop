from django import forms
from .models import ShippingAddress, Order, OrderItem

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['city', 'address', 'email', 'zip_code', 'country']
        exclude = ['user']