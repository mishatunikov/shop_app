import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend.settings')
os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': 'true'})
django.setup()

import logging
from asgiref.sync import sync_to_async

from django.db.models import Sum, Count, OuterRef, Exists, Subquery
from django.db.models import IntegerField

from shop.models import TgUser, Category, Subcategory, Item, ShoppingCartItems

logger = logging.getLogger(__name__)


@sync_to_async
def add_or_create_user(user_id: int, **kwargs) -> TgUser:
    """Add new user to db."""

    user, created = TgUser.objects.get_or_create(
        tg_id=user_id, defaults=kwargs
    )

    if created:
        logger.info(f'Пользователь tg_id={user_id} был добавлен в бд.')

    else:
        logger.info(f'Пользователь tg_id={user_id} уже существует в бд.')

    return user


@sync_to_async
def get_active_categories():
    """Return active category, which have at least one item."""

    return (
        Category.objects.annotate(
            items_count=Count('subcategories__items', distinct=True)
        )
        .filter(items_count__gt=0)
        .values_list('name', flat=True)
    )


@sync_to_async
def get_active_subcategories(category_name: str):
    """Return active subcategory, which have at least on item."""

    return (
        Subcategory.objects.filter(category__name=category_name)
        .annotate(count_items=Count('items'))
        .filter(count_items__gt=0)
        .values_list('name', flat=True)
    )


@sync_to_async
def get_items(subcategory_name: str, tg_id: int):
    """Return subcategory items."""

    cart_items = ShoppingCartItems.objects.filter(
        item=OuterRef('pk'), user__tg_id=tg_id
    )

    return Item.objects.filter(subcategory__name=subcategory_name).annotate(
        in_cart=Exists(cart_items),
        amount=Subquery(
            cart_items.values('amount'), output_field=IntegerField()
        ),
    )


@sync_to_async
def increase_shopping_cart(tg_id, item_id, amount):
    """Add item to user shopping cart."""

    instance = ShoppingCartItems(user_id=tg_id, item_id=item_id, amount=amount)
    instance.save()
    return instance


@sync_to_async
def decrease_shopping_cart(user_id, item_id):
    """Remove item from user shopping cart."""

    return ShoppingCartItems.objects.get(
        user_id=user_id, item_id=item_id
    ).delete()
