from django.conf import settings


def count_product_in_cart(request):
    cart_session = request.session.get(settings.CART_SESSION_ID)

    if cart_session:
        count_product_in_cart = sum([item['quantity'] for item in cart_session.values()])
    else:
        count_product_in_cart = 0

    return {'count_product_in_cart': count_product_in_cart}


def count_product_in_wishlist(request):
    wishlist_session = request.session.get(settings.WISHLIST_SESSION_ID)

    if wishlist_session:
        count_product_in_wishlist = len([item for item in wishlist_session.keys()])
    else:
        count_product_in_wishlist = 0

    return {'count_product_in_wishlist': count_product_in_wishlist}
