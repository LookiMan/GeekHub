from django.db import models

from telegram_bot.utils import set_default_image
from chat.models import Staff 


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


class Chat(models.Model):
    ucid = models.AutoField(
        "ucid",
        primary_key=True, 
        unique=True,
        help_text="Уникальный идентификатор чата в базе данных",
    )

    id = models.BigIntegerField(
        "id",
        help_text="Идентификатор чата в telegram",
    )

    is_closed = models.BooleanField(
        "is_closed",
        default=False,
        help_text="Является ли чат закрытым",
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

    type = models.CharField(
        "type",
        max_length=32,
        blank=True,
        help_text="Тип чата",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="chats"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        first_name = self.first_name or ""
        last_name = self.last_name or ""
        username = self.username or ""
        return f"Telegram chat: {first_name} {last_name} @{username} ({self.id})"

    class Meta:
        verbose_name = "Telegram чат"
        verbose_name_plural = "Telegram чаты"


class Message(models.Model):
    umid = models.AutoField(
        "umid",
        primary_key=True, 
        unique=True,
        help_text="Уникальный идентификатор сообщения в базе данных",
    )

    id = models.BigIntegerField(
        "id",
        help_text="Идентификатор сообщения в telegram",
    )

    chat = models.ForeignKey(
        Chat, 
        on_delete=models.CASCADE,
        related_name="messages"
    )

    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
    )

    staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
    )

    reply_to_message = models.ForeignKey(
        "Message", 
        on_delete=models.SET_NULL, 
        null=True,
    )

    text = models.TextField(
        "text",
        blank=True,
        null=True,
        help_text="Текст сообщения",
    )

    photo = models.ImageField(
        blank=True,
        null=True,
        help_text="Изображение от пользователя",
    )

    document = models.FileField(
        blank=True,
        null=True,
        help_text="Файл от пользователя",
    )

    file_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Имя файла отправленого пользователем",
    )

    caption = models.TextField(
        blank=True,
        null=True,
        help_text="Описание файла/фото от пользователя",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.photo:
            self.photo.delete(save=False)

        if self.document:
            self.document.delete(save=False)

        super().delete(*args, **kwargs)

    def __str__(self):
        preview_text = self.text[:100] if self.text else self.caption
        return f"Telegram message ({self.id}): {preview_text}"

    class Meta:
        verbose_name = "Telegram сообщение"
        verbose_name_plural = "Telegram сообщения"
