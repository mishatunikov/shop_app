from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from shop import consts


class CreatedUpdatedAt(models.Model):
    """Abstract model with creation and update datetime."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class BaseName(models.Model):
    """Abstract model with name field."""

    name = models.CharField(
        max_length=consts.MAX_NAME_LENGTH, verbose_name='название'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class TgUser(CreatedUpdatedAt):
    """Telegram User model."""

    tg_id = models.PositiveBigIntegerField(
        primary_key=True,
        verbose_name='tg_id',
    )
    username = models.CharField(
        max_length=consts.MAX_NAME_LENGTH,
        verbose_name='псевдоним',
        null=True,
        unique=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=consts.MAX_NAME_LENGTH,
        blank=True,
        null=True,
        verbose_name='имя',
    )
    last_name = models.CharField(
        max_length=consts.MAX_NAME_LENGTH,
        null=True,
        blank=True,
        verbose_name='фамилия',
    )
    is_active = models.BooleanField(default=True, verbose_name='активен')

    class Meta(CreatedUpdatedAt.Meta):
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.__class__.__name__}(tg_id={self.tg_id})'


class Category(BaseName, CreatedUpdatedAt):
    """Category model."""

    name = models.CharField(
        max_length=consts.MAX_NAME_LENGTH, verbose_name='название', unique=True
    )

    class Meta(BaseName.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Subcategory(BaseName, CreatedUpdatedAt):
    """Subcategory model."""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='категория',
        related_name='subcategories',
    )

    class Meta(BaseName.Meta):
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'
        constraints = [
            UniqueConstraint(
                fields=('name', 'category'), name='unique_name_category'
            )
        ]


class Item(BaseName, CreatedUpdatedAt):
    """Item model."""

    description = models.TextField(
        max_length=consts.MAX_TEXT_LENGTH, verbose_name='описание'
    )
    image = models.ImageField(upload_to='items', verbose_name='изображение')
    price = models.DecimalField(
        max_digits=consts.DECIMAL_MAX_DIGITS,
        decimal_places=consts.DECIMAL_PLACES,
        verbose_name='цена (р.)',
        validators=[
            MinValueValidator(consts.MIN_ITEM_PRICE),
            MaxValueValidator(consts.MAX_ITEM_PRICE),
        ],
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='подкатегория',
    )

    class Meta(BaseName.Meta):
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'
        constraints = [
            UniqueConstraint(
                fields=('name', 'subcategory'), name='unique_name_subcategory'
            )
        ]


class ShoppingCartItems(CreatedUpdatedAt):
    """Binds users and items, realize shopping cart."""

    user = models.ForeignKey(
        TgUser, on_delete=models.CASCADE, related_name='shopping_cart_items'
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='shopping_cart'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(consts.MIN_ITEM_AMOUNT),
            MaxValueValidator(consts.MAX_ITEM_AMOUNT),
        ]
    )

    class Meta(CreatedUpdatedAt.Meta):
        verbose_name = 'товар корзины'
        verbose_name_plural = 'Товары корзины'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'item'),
                name='unique_item_shopping_cart',
            )
        ]


class QuestionAnswer(models.Model):
    """Contains questions and answer to them."""

    question = models.CharField(
        max_length=consts.MAX_LENGTH_QUESTION,
        unique=True,
        verbose_name='вопрос',
    )
    answer = models.CharField(
        max_length=consts.MAX_LENGTH_ANSWER, verbose_name='ответ'
    )

    class Meta:
        verbose_name = 'вопрос-ответ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return self.question
