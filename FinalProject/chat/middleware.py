import os
from datetime import datetime

import django
from django.db import close_old_connections
from django.contrib.auth.models import AnonymousUser
from django.conf import settings

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

import jwt

from chat.models import Staff


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=settings.ALGORITHM)
    except:
        return AnonymousUser()

    token_exp = datetime.fromtimestamp(payload['exp'])
    if token_exp < datetime.utcnow():
        return AnonymousUser()

    try:
        staff = Staff.objects.get(id=payload['id'])
    except Staff.DoesNotExist:
        return AnonymousUser()

    return staff


class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()

        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split(
                "&")))).get('token', None)
        except ValueError:
            token_key = None

        scope['user'] = await get_user(token_key)

        return await super().__call__(scope, receive, send)
