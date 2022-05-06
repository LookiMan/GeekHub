from django.db import models


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

    image = models.URLField(
        "user image",
        max_length=200,
        blank=True,
        null=True,
        help_text="Изображение пользователя",
    )

    created_at = models.DateTimeField(
        "created_at",
        auto_now_add=True,
        help_text="Дата сохранения пользователя в базу данных",
    )

    def __str__(self):
        first_name = self.first_name or ""
        last_name = self.last_name or ""
        username = "@" + self.username if self.username else ""
        return f"Telegram user: {first_name} {last_name} {username} ({self.id})"

    class Meta:
        verbose_name = "Telegram пользователя"
        verbose_name_plural = "Telegram пользователи"
