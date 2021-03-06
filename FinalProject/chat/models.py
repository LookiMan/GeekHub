from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from django.db import models
import jwt

from telegram_bot.models import User


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

    is_archived = models.BooleanField(
        "is_archived",
        default=False,
        help_text="Является ли чат заархивированным",
    )

    archived_at = models.DateTimeField(
        "archived_at",
        blank=True,
        null=True,
        help_text="Дата архивации чата",
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

    @property
    def archived_at_formatted(self):
        if self.archived_at:
            return self.archived_at.strftime("%d-%m-%Y %H:%M:%S")
        return "[Дата не установлена]"

    def __str__(self):
        first_name = self.first_name or ""
        last_name = self.last_name or ""
        username = "@" + self.username if self.username else ""
        state = f"ARCHIVED {self.archived_at_formatted}" if self.is_archived else "ACTIVE"
        return f"Сhat: {first_name} {last_name} {username} ({self.id}) {state}"

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
        "filename",
        max_length=255,
        blank=True,
        null=True,
        help_text="Имя файла отправленого пользователем",
    )

    caption = models.TextField(
        "caption",
        blank=True,
        null=True,
        help_text="Описание файла/фото от пользователя",
    )

    edited_text = models.TextField(
        "edited_text",
        blank=True,
        null=True,
        help_text="Отредактированный текст сообщения",
    )

    is_edited = models.BooleanField(
        "is_edited",
        default=False,
        help_text="Является ли сообщение отредактированным",
    )

    is_deleted = models.BooleanField(
        "is_deleted",
        default=False,
        help_text="Является ли сообщение удаленным",
    )

    date = models.DateTimeField(
        "date",
        blank=True,
        null=True,
        help_text="Время получения сообщения в telegram",
    )

    created_at = models.DateTimeField(
        "created_at",
        auto_now_add=True,
        help_text="Время создания сообщения в базе данных",
    )

    def __str__(self):
        if self.text:
            preview_text = self.text[:100] if self.text else self.caption
        elif self.photo:
            preview_text = f'<i>Фото</i>'
        elif self.document:
            preview_text = f'<i>Документ:</i> {self.file_name}'
        else:
            preview_text = '<i>Отсутствует</i>'

        return mark_safe(f"Telegram message ({self.id}): {preview_text}")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
