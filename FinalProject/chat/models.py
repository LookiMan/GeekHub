from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
import jwt


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
