from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from chat.models import Staff, Chat, Message
from chat.forms import CustomStaffCreationForm, CustomStaffChangeForm


class CustomModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))


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


@admin.register(Chat)
class ChatAdmin(CustomModelAdmin):
    readonly_fields = ("ucid", "id")

    actions = ("make_closed", "make_opened")

    def make_closed(self, request, queryset):
        queryset.update(is_blocked=True)
    make_closed.short_description = "Отметить выбранные чаты как закрытые"

    def make_opened(self, request, queryset):
        queryset.update(is_blocked=False)
    make_opened.short_description = "Отметить выбранные чаты как открытые"


@admin.register(Message)
class MessageAdmin(CustomModelAdmin):
    readonly_fields = ("umid", "id")
