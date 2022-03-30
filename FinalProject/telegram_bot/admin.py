from django.contrib import admin
from django.utils.safestring import mark_safe

from telegram_bot.models import TelegramUser, TelegramChat, TelegramMessage


class CustomModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))


@admin.register(TelegramUser)
class TelegramUserAdmin(CustomModelAdmin):
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
        "language_code",
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
                (("first_name", "last_name"),)
        }
        ),
        ("Профиль", {
            "fields":
                (("username", "image", "language_code"),)
        }
        ),
        ("Персональние данные", {
            "fields":
            (("uuid", "id", "is_bot"),)
        }
        ),
    )

    search_fields = ("id", "username", "first_name", "last_name")

    actions = ("make_blocked", "make_unblocked")

    def preview_user_image(self, obj):
        if obj.image:
            return mark_safe(f'<div> <img src="{obj.image_url}" style="width: 50px; height: 50px; background-size: cover; border-radius: 50%;"></div>')
        else:
            return '[Фото не загружено]'

    def make_blocked(self, request, queryset):
        queryset.update(is_blocked=True)
    make_blocked.short_description = "Отметить выбранных пользователей как заблокированых"

    def make_unblocked(self, request, queryset):
        queryset.update(is_blocked=False)
    make_unblocked.short_description = "Отметить выбранных пользователей как разблокированых"


@admin.register(TelegramChat)
class TelegramChatAdmin(CustomModelAdmin):
    readonly_fields = ("ucid", "id")

    actions = ("make_closed", "make_opened")

    def make_closed(self, request, queryset):
        queryset.update(is_blocked=True)
    make_closed.short_description = "Отметить выбранные чаты как закрытые"

    def make_opened(self, request, queryset):
        queryset.update(is_blocked=False)
    make_opened.short_description = "Отметить выбранные чаты как открытые"


@admin.register(TelegramMessage)
class TelegramMessageAdmin(CustomModelAdmin):
    readonly_fields = ("umid", "id")
