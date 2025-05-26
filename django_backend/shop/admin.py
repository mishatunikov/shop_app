from django.contrib import admin
from django.db.models import Count, Sum

from shop.models import (
    Category,
    Item,
    ShoppingCartItems,
    Subcategory,
    TgUser,
    QuestionAnswer,
)


class InlineShoppingCart(admin.TabularInline):
    model = ShoppingCartItems
    extra = 0


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'subcategory')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('subcategory',)
    search_fields = ('name',)
    list_editable = ('price', 'subcategory')


class ItemInline(admin.StackedInline):
    model = Item
    extra = 0


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'count_items')
    readonly_fields = ('created_at', 'updated_at', 'count_items')
    search_fields = ('name',)
    list_filter = ('category__name',)
    inlines = (ItemInline,)

    def get_queryset(self, request):
        return Subcategory.objects.prefetch_related('items').annotate(
            count_items=Count('items')
        )

    @admin.display(description='количество товаров', ordering='count_items')
    def count_items(self, obj):
        return obj.count_items


class SubCategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_subcategory')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at', 'count_subcategory')
    inlines = (SubCategoryInline,)

    def get_queryset(self, request):
        return Category.objects.prefetch_related('subcategories').annotate(
            count_subcategory=Count('subcategories')
        )

    @admin.display(
        description='количество подкатегорий', ordering='count_subcategory'
    )
    def count_subcategory(self, obj):
        return obj.count_subcategory


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = (
        'tg_id',
        'username',
        'first_name',
        'last_name',
        'is_active',
        'count_items',
    )
    readonly_fields = ('created_at', 'updated_at', 'count_items')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = (
        'tg_id',
        'username',
    )
    inlines = (InlineShoppingCart,)

    def get_queryset(self, request):
        return TgUser.objects.prefetch_related('shopping_cart_items').annotate(
            items_count=Sum('shopping_cart_items__amount')
        )

    @admin.display(description='Товаров в корзине', ordering='items_count')
    def count_items(self, obj):
        return obj.items_count


admin.site.empty_value_display = 'Не задано'
admin.site.register(QuestionAnswer)
