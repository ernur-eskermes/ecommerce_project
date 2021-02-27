from django.shortcuts import render, redirect
from django.urls import reverse

from cart.cart import Cart
from coupons.views import coupon_clear
from .forms import OrderCreateForm
from .models import OrderItem


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            if request.user.is_authenticated:
                order.user = request.user

            order.save()

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])

            cart.clear()
            coupon_clear(request)

            request.session['order_id'] = order.id

            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order_create.html', {'cart': cart,
                                                        'form': form})
