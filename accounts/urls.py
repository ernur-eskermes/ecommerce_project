from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.account, name='account'),

    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
