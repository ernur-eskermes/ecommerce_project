from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserDataChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': _('Имя'), 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': _('Фамилия'), 'class': 'form-control'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')
        field_classes = {'username': UsernameField}
