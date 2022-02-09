from attr import field
from django import forms

from store.models import Product


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput)


class EditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'description', 'price')
