from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem


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
    print('Complete order called with data:', request.POST)
    if request.POST.get('action') == 'payment':
        print('Payment action detected')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        cart = Cart(request)
        total_price = cart.get_total_price()

        print('Creating or getting shipping address for user', request.user)
        shipping_address, _ = ShippingAddress.objects.get_or_create(
            user=request.user,
            defaults={
                'name': name,
                'email': email,
                'address': address,
                'city': city,
                'country': country,
                'zip_code': zipcode
            })
        print('Created or retrieved shipping address:', shipping_address)

        order = None
        if request.user.is_authenticated:
            print('Creating order for authenticated user', request.user)
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                amount=total_price
            )
        else:
            print('Creating order for guest user')
            order = Order.objects.create(
                shipping_address=shipping_address,
                amount=total_price
            )
        print('Created order:', order)

        for item in cart:
            print('Creating order item for product', item['product'])
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['qty'],
                user=request.user if request.user.is_authenticated else None
            )
        print('Created all order items')

        return JsonResponse({'success': True})
