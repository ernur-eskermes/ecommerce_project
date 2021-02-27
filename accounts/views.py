from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView

from orders.models import Order
from .forms import UserDataChangeForm, RegisterForm


def change_user_password(request):
    password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
    if password_change_form.is_valid():
        password_change_form.save()
        update_session_auth_hash(request, password_change_form.user)
        messages.success(request, _('Ваш пароль изменен.'))
        return redirect('accounts:account')
    else:
        messages.error(request, _('Введите правильные данные'))


def change_user_data(request):
    form = UserDataChangeForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, _('Ваши данные изменены.'))
        return redirect('accounts:account')
    else:
        messages.error(request, _('Введите правильные данные.'))


@login_required
def account(request):
    orders = Order.objects.filter(user=request.user)
    if request.method == 'POST' and 'password_change_button' in request.POST:
        change_user_password(request)
    elif request.method == 'POST' and 'user_update_button' in request.POST:
        change_user_data(request)
    else:
        form = UserDataChangeForm(instance=request.user)
        password_change_form = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/my-account.html',
                      {'orders': orders, 'form': form, 'password_change_form': password_change_form})
    return redirect('accounts:account')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('store:product_list')

    def form_valid(self, form):
        view = super(RegisterView, self).form_valid(form)
        username, password = form.cleaned_data['username'], form.cleaned_data['password1']
        user = authenticate(username=username, password=password)

        login(self.request, user)
        return view


class MyLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if request.POST.get('remember_me', None):
                request.session.set_expiry(settings.KEEP_LOGGED_DURATION)  # 10 day
            else:
                request.session.set_expiry(0)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class MyLogoutView(LogoutView):
    pass
