from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from coupons.models import Coupon
from store.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    postal_code = models.CharField(max_length=255, verbose_name='Zip код')
    city = models.CharField(max_length=255, verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    braintree_id = models.CharField(max_length=255, blank=True, verbose_name='Id транзакций')

    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL,
                               verbose_name='Купон')
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   verbose_name='Скидка %')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_price(self):
        total_price = sum(item.get_cost() for item in self.items.all())
        return total_price - total_price * (self.discount / Decimal(100))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Продукт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Заказ - Продукт'
        verbose_name_plural = 'Заказы - Продукты'
