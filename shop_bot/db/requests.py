import os

import django
from django.db.models import Sum, Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend.settings')
os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': 'true'})
django.setup()

import logging
from asgiref.sync import sync_to_async

from shop.models import TgUser, Category


logger = logging.getLogger(__name__)


@sync_to_async
def add_or_create_user(user_id: int, **kwargs) -> TgUser:
    user, created = TgUser.objects.get_or_create(
        tg_id=user_id, defaults=kwargs
    )

    if created:
        logger.info(f'Пользователь tg_id={user_id} был добавлен в бд.')

    else:
        logger.info(f'Пользователь tg_id={user_id} уже существует в бд.')

    return user


@sync_to_async
def get_categories():
    return (
        Category.objects.annotate(
            items_count=Count('subcategories__items', distinct=True)
        )
        .filter(items_count__gt=0)
        .values_list('name', flat=True)
    )
