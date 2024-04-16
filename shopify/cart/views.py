from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shop.models import ProductProxy
from django.http import JsonResponse
from django.contrib import messages
def cart_view(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'cart/cart.html', context = context)

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        product = get_object_or_404(ProductProxy, id=product_id)
        cart.add(product=product, qty=product_qty)
        
        cart_qty = cart.__len__()
        
        response = JsonResponse({'qty': cart_qty,
                                 'product':product.title})
        messages.success(request, 'Товар успешно добавлен в корзину.')
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()
        response = JsonResponse({'qty': cart_qty, 
                                 'total': cart_total})
        messages.success(request, 'Товар успешно удален из корзины')
        return response
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, qty=product_qty)
        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()
        response = JsonResponse({'qty': cart_qty, 
                                 'total': cart_total})
        messages.success(request, 'Корзина успешно обновлена.')
        return response