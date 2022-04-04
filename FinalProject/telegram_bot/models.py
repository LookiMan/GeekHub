from django.db import models

from telegram_bot.utils import set_default_image


class User(models.Model):
    uuid = models.AutoField(
        "uuid",
        primary_key=True,
        unique=True,
        help_text="Уникальный идентификатор пользователя в базе данных",
    )

    id = models.BigIntegerField(
        "id",
        help_text="Идентификатор пользователя в telegram",
    )

    is_bot = models.BooleanField(
        "is_bot",
        default=False,
        help_text="Является ли пользователь ботом",
    )

    is_blocked = models.BooleanField(
        "is_blocked",
        default=False,
        help_text="Заблокирован ли пользователь",
    )

    first_name = models.CharField(
        "first_name",
        max_length=128,
        help_text="Имя пользователя",
    )

    last_name = models.CharField(
        "last_name",
        max_length=128,
        blank=True,
        null=True,
        help_text="Фамилия пользователя",
    )

    username = models.CharField(
        "username",
        max_length=64,
        blank=True,
        null=True,
        help_text="Псевдоним пользователя (необязательный)",
    )

    image = models.ImageField(
        blank=True,
        null=True,
        default=set_default_image,
        help_text="Изображение пользователя",
    )

    language_code = models.CharField(
        "language_code",
        blank=True,
        null=True,
        max_length=16,
        help_text="Код языка системы",
    )

    created_at = models.DateTimeField(
        "created_at",
        auto_now_add=True,
        help_text="Дата сохранения пользователя в базу данных",
    )

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)

        super().delete(*args, **kwargs)

    def __str__(self):
        first_name = self.first_name or ""
        last_name = self.last_name or ""
        username = self.username or ""
        return f"Telegram user: {first_name} {last_name} @{username} ({self.id})"

    class Meta:
        verbose_name = "Telegram пользователя"
        verbose_name_plural = "Telegram пользователи"
