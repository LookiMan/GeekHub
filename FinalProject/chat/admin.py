from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from chat.models import Staff
from chat.forms import CustomStaffCreationForm, CustomStaffChangeForm


@admin.register(Staff)
class CustomStaffAdmin(UserAdmin):
    add_form = CustomStaffCreationForm
    form = CustomStaffChangeForm
    model = Staff

    list_display = (
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )

    list_filter = (
        ("is_staff", admin.BooleanFieldListFilter),
        ("is_active", admin.BooleanFieldListFilter),
        "username",
        "email",
    )

    fieldsets = (
        ("Авторизация", {
            "fields":
                (("username", "email"),)
        }
        ),
        ("Разрешения", {
            "fields":
                (("is_staff", "is_active"),)
        }
        ),
        ("Персональние данные", {
            "fields":
                (("first_name", "last_name"),)
        }
        ),
    )

    add_fieldsets = (
        ("Регистрация нового сотрудника", {
            "classes": ("wide",),
            "fields":
                (
                    "username",
                    ("password1", "password2"),
            )
        },
        ),
    )

    search_fields = ("username",)
    ordering = ("username",)

    actions = ("make_active", "make_inactive")

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Отметить выбранных сотрудников как активные"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Отметить выбранных сотрудников как неактивные"
