from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('categories/<slug:category_slug>', views.product_list, name='product_list_by_category'),
    path('publishers/<slug:publisher_slug>', views.product_list, name='product_list_by_publisher'),
    path('contact/', views.contact, name='contact'),
    path('<int:pk>/<slug:slug>/', views.detail, name='detail'),
]
