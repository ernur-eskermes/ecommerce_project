from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart'),
    path('wishlist/', views.wishlist_detail, name='wishlist'),
    path('update_cart/', views.update_cart, name='update_cart'),
]
