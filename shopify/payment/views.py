import uuid
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from decimal import Decimal
import stripe
from yookassa import Configuration, Payment
from django.contrib import messages
from django.urls import reverse
from .forms import ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem
from .exchange_rate import get_exchange_rate
import asyncio

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.publishable_key = settings.STRIPE_PUBLISHABLE_KEY
stripe.api_version = settings.STRIPE_API_VERSION

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

@login_required(login_url='account:login')
def shipping(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = None
    form = ShippingAddressForm(instance=shipping_address)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('account:home')

    return render(request, 'payment/shipping.html', {'form': form})


def checkout(request):
    if request.user.is_authenticated:
        shipping_address = get_object_or_404(
            ShippingAddress, user=request.user)
        if shipping_address:
            return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})
    return render(request, 'payment/checkout.html')


def payment_success(request):
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]
    return render(request, 'payment/payment_success.html')


def payment_fail(request):
    return render(request, 'payment/payment_fail.html')


def complete_order(request):
    if request.method == 'POST':
        payment_type = request.POST.get('stripe-payment', 'yookassa-payment')

        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        cart = Cart(request)
        total_price = cart.get_total_price()
        for item in cart:
            print(item)

        if payment_type == 'stripe-payment':
            shipping_address, _ = ShippingAddress.objects.get_or_create(
                user=request.user if request.user.is_authenticated else None,
                defaults={
                    'name': name,
                    'email': email,
                    'address': address,
                    'city': city,
                    'country': country,
                    'zip_code': zipcode
                })
            session_data = {
                'mode': 'payment',
                'success_url': request.build_absolute_uri(reverse('payment:payment-success')),
                'cancel_url': request.build_absolute_uri(reverse('payment:payment-fail')),
                'line_items': []
            }

            if request.user.is_authenticated:
                order = Order.objects.create(
                    user=request.user,
                    shipping_address=shipping_address,
                    amount=total_price
                )
            else:
                order = Order.objects.create(
                    shipping_address=shipping_address,
                    amount=total_price
                )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['qty'],
                    user=request.user if request.user.is_authenticated else None
                )
                session_data['line_items'].append({
                    'price_data': {
                        'unit_amount': int(item['price'] * Decimal(100)),
                        'currency': 'usd',
                        'product_data': {
                                    'name': item['product']
                        },
                    },
                    'quantity': item['qty'],
                })
            try:
                session = stripe.checkout.Session.create(**session_data)
                return redirect(session.url, code=303)
            except stripe.error.StripeError as e:
                messages.error(request, e.user_message)
                return redirect('shop:products')
            
        elif payment_type == 'yookassa-payment':
            idempotency_key = uuid.uuid4()
            currency = 'RUB'
            discription = 'Оплата заказа'
            payment = Payment.create(
                {
                    'amount': {
                        'value': str(total_price* Decimal(asyncio.run(get_exchange_rate('USD', 'RUB')))),
                        'currency': currency
                    },
                    'confirmation': {
                        'type': 'redirect',
                        'return_url': request.build_absolute_uri(reverse('payment:payment-success')),
                    },
                    'capture': True,
                    'description': discription,
                    'test': True,
                }, idempotency_key = idempotency_key
            )
            shipping_address, _ = ShippingAddress.objects.get_or_create(
                user=request.user if request.user.is_authenticated else None,
                defaults={
                    'name': name,
                    'email': email,
                    'address': address,
                    'city': city,
                    'country': country,
                    'zip_code': zipcode
                })
            confirmation_url = payment.confirmation.confirmation_url
            if request.user.is_authenticated:
                order = Order.objects.create(
                    user=request.user,
                    shipping_address=shipping_address,
                    amount=total_price
                )
            else:
                order = Order.objects.create(
                    shipping_address=shipping_address,
                    amount=total_price
                )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['qty'],
                    user=request.user if request.user.is_authenticated else None
                )
                return redirect(confirmation_url)