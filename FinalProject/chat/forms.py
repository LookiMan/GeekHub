from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from chat.models import Staff


class LoginStaffForm(forms.Form):
    login = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={"placeholder": "введите логин"}),
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "введите пароль"}),
    )


class RegisterStaffForm(forms.ModelForm):
    login = forms.CharField(
        label="Логин",
        help_text="Придумайте уникальный логин для авторизации сотрудника",
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Придумайте пароль для авторизации сотрудника",
    )

    password2 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Повторите тот же самый пароль еще раз для проверки",
    )

    username = forms.CharField(
        label="Уникальный username сотрудника",
        help_text="Придумайте уникальный username сотрудника",
    )

    first_name = forms.CharField(
        label="Имя сотрудника",
        help_text="Укажите имя сотрудника",
    )

    last_name = forms.CharField(
        label="Фамилия сотрудника",
        help_text="Укажите фамилию сотрудника",
    )

    def clean_password1(self):
        password1 = self.cleaned_data["password1"]

        if password1:
            password_validation.validate_password(password1)

        return password1

    def clean(self):
        super().clean()

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            errors = {"password2": forms.ValidationError(
                "Введенные пароли не совпадают",
                code="password_mismach",
            )
            }

            raise forms.ValidationError(errors)

    def save(self, commit=True):
        employee = super().save(commit=False)
        employee.set_password(self.cleaned_data["password1"])

        employee.is_active = True

        if commit:
            employee.save()

        return employee

    class Meta:
        model = Staff
        fields = (
            "login",
            "password1",
            "password2",
            "username",
            "first_name",
            "last_name"
        )


class ChangeStaffInfoForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Имя",
        help_text="Имя сотрудника",
        required=True,
    )

    last_name = forms.CharField(
        label="Фамилия",
        help_text="Фамилия сотрудника",
        required=True,
    )

    class Meta(UserCreationForm):
        model = Staff
        fields = (
            "login",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
        )


class CustomStaffCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Staff
        fields = ("username",)


class CustomStaffChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = Staff
        fields = ("username",)


class UploadFileForm(forms.Form):
    ucid = forms.CharField()

    photo = forms.FileField(required=False)
    document = forms.FileField(required=False)
    file_name = forms.CharField(required=False)
    reply_to_message_id = forms.IntegerField(required=False)
    caption = forms.CharField(required=False)
    message_id = forms.IntegerField(required=False)
    date = forms.IntegerField(required=False)
