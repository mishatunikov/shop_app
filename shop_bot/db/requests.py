import os
import sys
from decimal import Decimal
from pathlib import Path

import django

DJANGO_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(DJANGO_BACKEND_DIR / 'django_backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend.settings')
os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': 'true'})
django.setup()

import logging
from asgiref.sync import sync_to_async

from django.db.models import (
    Sum,
    Count,
    OuterRef,
    Exists,
    Subquery,
    ExpressionWrapper,
    F,
    QuerySet,
)
from django.db.models import IntegerField, DecimalField

from shop.models import (
    TgUser,
    Category,
    Subcategory,
    Item,
    ShoppingCartItems,
    QuestionAnswer,
)

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
def get_active_categories() -> QuerySet:
    """Return active category, which have at least one item."""

    return (
        Category.objects.annotate(
            items_count=Count('subcategories__items', distinct=True)
        )
        .filter(items_count__gt=0)
        .values_list('name', flat=True)
    )


@sync_to_async
def get_active_subcategories(category_name: str) -> QuerySet:
    """Return active subcategory, which have at least on item."""

    return (
        Subcategory.objects.filter(category__name=category_name)
        .annotate(count_items=Count('items'))
        .filter(count_items__gt=0)
        .values_list('name', flat=True)
    )


@sync_to_async
def get_items(subcategory_name: str, tg_id: int) -> QuerySet:
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
def increase_shopping_cart(tg_id, item_id, amount) -> ShoppingCartItems:
    """Add item to user shopping cart."""

    instance = ShoppingCartItems(user_id=tg_id, item_id=item_id, amount=amount)
    instance.save()
    return instance


@sync_to_async
def decrease_shopping_cart(user_id, item_id) -> tuple[int, dict]:
    """Remove item from user shopping cart."""

    return ShoppingCartItems.objects.get(
        user_id=user_id, item_id=item_id
    ).delete()


@sync_to_async
def get_shopping_cart_items(tg_id: int) -> tuple[QuerySet, bool, int, Decimal]:
    """Return user shopping cart information."""

    subquery = ShoppingCartItems.objects.filter(
        item=OuterRef('pk'),
        user_id=tg_id,
    ).values('amount')

    items = (
        Item.objects.filter(shopping_cart__user=tg_id)
        .annotate(
            amount=Subquery(
                subquery,
                output_field=IntegerField(),
            )
        )
        .annotate(
            total_item_price=ExpressionWrapper(
                F('price') * F('amount'), output_field=DecimalField()
            )
        )
    )

    total_amount = items.aggregate(total=Sum('amount'))['total'] or 0
    total_price = items.aggregate(total=Sum('total_item_price'))['total'] or 0

    return items, items.exists(), total_amount, total_price


@sync_to_async
def clean_shopping_cart(tg_id: int) -> None:
    """Clean shopping cart."""

    ShoppingCartItems.objects.filter(user_id=tg_id).delete()


@sync_to_async()
def delete_item_from_cart(tg_id: int, item_id: int) -> None:
    """Delete item from shopping cart."""

    ShoppingCartItems.objects.filter(user_id=tg_id, item_id=item_id).delete()


@sync_to_async()
def get_user_cart_info(tg_id: int) -> bool:
    """Check shopping cart for void."""

    return TgUser.objects.get(tg_id=tg_id).shopping_cart_items.exists()


@sync_to_async
def change_item_amount(tg_id: int, item_id: int, amount) -> None:
    """Change item amount in shopping cart."""

    instance = ShoppingCartItems.objects.get(user_id=tg_id, item_id=item_id)
    instance.amount = amount
    instance.save()


@sync_to_async
def get_faq() -> tuple[tuple, bool]:
    queryset = QuestionAnswer.objects.all()
    exist = queryset.exists()
    questions = (
        () if not exist else queryset.values_list('question', flat=True)
    )
    return questions, queryset.exists()


@sync_to_async
def get_answer(question: str) -> str:
    return QuestionAnswer.objects.get(question=question).answer
