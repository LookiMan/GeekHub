from django.contrib import admin
from django.utils.safestring import mark_safe

from chat.admin import CustomModelAdmin
from telegram_bot.models import User


@admin.register(User)
class UserAdmin(CustomModelAdmin):
    readonly_fields = ("uuid", "id", "is_bot")

    list_display = (
        "uuid",
        "id",
        "is_bot",
        "is_blocked",
        "first_name",
        "last_name",
        "username",
        "preview_user_image",
        "created_at",
    )

    list_filter = (
        ("is_bot", admin.BooleanFieldListFilter),
        ("is_blocked", admin.BooleanFieldListFilter),
        "id",
        "username",
    )

    fieldsets = (
        ("Персональные данные", {
            "fields":
                (("first_name", "last_name", "username"),)
        }
        ),
        ("Профиль", {
            "fields":
                (("image", "is_blocked"),)
        }
        ),
        ("Персональные данные", {
            "fields":
            (("uuid", "id", "is_bot"),)
        }
        ),
    )

    search_fields = ("id", "username", "first_name", "last_name")

    actions = ("make_blocked", "make_unblocked")

    def preview_user_image(self, obj):
        if obj.image:
            return mark_safe(f'<div> <img src="{obj.image}" style="width: 50px; height: 50px; background-size: cover; border-radius: 50%;"></div>')
        else:
            return '[Фото не загружено]'

    def make_blocked(self, request, queryset):
        queryset.update(is_blocked=True)
    make_blocked.short_description = "Отметить выбранных пользователей как заблокированы"

    def make_unblocked(self, request, queryset):
        queryset.update(is_blocked=False)
    make_unblocked.short_description = "Отметить выбранных пользователей как разблокированы"
