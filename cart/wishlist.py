from decimal import Decimal

from django.conf import settings

from store.models import Product


class Wishlist(object):
    def __init__(self, request):
        """Инициализация списка желаний"""
        self.session = request.session
        wishlist = self.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            wishlist = self.session[settings.WISHLIST_SESSION_ID] = {}
        self.wishlist = wishlist

    def add(self, product):
        """Добавить товар в список желаний."""
        product_id = str(product.id)
        if product_id not in self.wishlist:
            self.wishlist[product_id] = {
                'price': str(product.price)
            }
        self.save()

    def delete(self, product):
        """Удалить продукт из списка желаний."""
        product_id = str(product.id)
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save()

    def __iter__(self):
        """Перебирает элементы в списке желаний и получает продукты из базы данных."""
        product_ids = self.wishlist.keys()
        # get the product objects and add them to the wishlist
        products = Product.objects.filter(id__in=product_ids)
        wishlist = self.wishlist.copy()
        for product in products:
            wishlist[str(product.id)]['product'] = product
        for item in wishlist.values():
            item['price'] = Decimal(item['price'])
            yield item

    def __len__(self):
        """Подсчитает количество всех товаров в списке желаний."""
        return Product.objects.filter(id__in=self.wishlist.keys()).count()

    def save(self):
        """Отмечает сеанс как 'измененный', чтобы убедиться, что он будет сохранен"""
        self.session.modified = True
