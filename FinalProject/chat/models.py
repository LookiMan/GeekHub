from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
import jwt

from telegram_bot.models import User

# https://habr.com/ru/post/538040/


class Staff(AbstractUser):
    login = models.CharField(
        "login",
        max_length=16,
        unique=True,
        help_text="Уникальный логин сотрудника",
    )

    username = models.CharField(
        "username",
        max_length=32,
        unique=True,
        help_text="Псевдоним сотрудника",
    )

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['username']

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        #Генерирует веб-токен JSON, в котором хранится идентификатор этого
        #пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            "id": self.pk,
            "exp": int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm="HS256")

        return token.decode("utf-8")

    def __str__(self):
        return f"User: {self.username}"

    class Meta(AbstractUser.Meta):
        verbose_name = "Сотрудника"
        verbose_name_plural = "Сотрудники"


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

    is_note = models.BooleanField(
        "is_note",
        default=False,
        help_text="Является ли чат заметкой",
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
        null=True,
        help_text="Тип чата",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="chats"
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
        return f"Сhat: {first_name} {last_name} @{username} ({self.id})"

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


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
        blank=True,
        null=True,
    )

    staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    reply_to_message = models.ForeignKey(
        "Message",
        on_delete=models.SET_NULL,
        blank=True,
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

    def __str__(self):
        preview_text = self.text[:100] if self.text else self.caption
        return f"Telegram message ({self.id}): {preview_text}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
