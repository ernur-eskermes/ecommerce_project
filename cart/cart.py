from decimal import Decimal

from django.conf import settings

from coupons.models import Coupon
from store.models import Product


class Cart(object):
    def __init__(self, request):
        """Инициализация корзины."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity):
        """Добавление товара в корзину или обновление его количество."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Отмечает сеанс как 'измененный', чтобы убедиться, что он будет сохранен."""
        self.session.modified = True

    def remove(self, product):
        """Уменьшить количество продукта на единицу."""
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            self.save()

    def delete(self, product):
        """Удалить продукт из корзины."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебирает элементы в корзины и получает продукты из базы данных."""
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчитает количество всех товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Получает общую цену."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):
        """Получает купон если он имеется"""
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """Получает скидку."""
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """Получает цену после скидки."""
        return self.get_total_price() - self.get_discount()

    def clear(self):
        """Удаляет корзину из сеанса."""
        del self.session[settings.CART_SESSION_ID]
        self.save()
