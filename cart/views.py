import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from coupons.forms import CouponApplyForm
from store.models import Product
from .cart import Cart
from .wishlist import Wishlist


def wishlist_detail(request):
    return render(request, 'cart/wishlist.html', {'wishlist': Wishlist(request)})


def cart_detail(request):
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/cart.html', {'coupon_apply_form': coupon_apply_form, 'cart': Cart(request)})


def update_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        product_id = data['productId']
        action = data['action']
        quantity = int(data['quantity'])
        update = data['update']

        product = get_object_or_404(Product, id=product_id)
        if update == 'cart':
            cart = Cart(request)
            if action == 'add':
                cart.add(product=product, quantity=quantity)
            elif action == 'remove':
                cart.remove(product)
            elif action == 'delete':
                cart.delete(product)
        elif update == 'wishlist':
            wishlist = Wishlist(request)
            if action == 'add':
                wishlist.add(product=product)
            elif action == 'delete':
                wishlist.delete(product)
        return JsonResponse('Item was added!', safe=False)
    else:
        return redirect('/')
