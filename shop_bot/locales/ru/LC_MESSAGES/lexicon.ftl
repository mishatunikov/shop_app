-brand_name = <b>SneakerStreet</b>

# general texts
counter-items =
    <b>{ $item_number }/{ $items_amount }</b>

# start dialog
main-menu-text =
    {$text_selection ->
        [one] <b>{ $name }</b>, добро пожаловать в { -brand_name }! 👋
        *[other] Вы вернулись в главное меню 🏠
    }

    <b>Выбери пункт меню 👇</b>

reference-text =
    ✨ <b>SneakerStreet</b> — твой гид в мире оригинального стиля.
    Мы продаём одежду, обувь и аксессуары от проверенных брендов.
    Только оригинал, только актуальные коллекции.

    Выбирай, заказывай — будь в потоке 🔥


# category dialog
category-text = Выбери интересующую категорию 👇
subcategory-text = Выбери интересующую подкатегорию 👇
item-info-text =
    <b>{ $name }</b>

    { $description }

    <b>Цена:</b> <i>{ $price }р.</i>

cart-add-confirm =
    <b>Добавить товар в корзину в количестве { $amount }шт.?</b>

# shopping cart dialog
shopping-cart-empty-text =
    <b>Ваша корзина пуста 😢</b>

    Время для того, чтобы это исправить 😉

shopping-cart-text =
    {$items_amount ->
        [one] <b>В вашей корзине { $items_amount } товар 🛍</b>
        [few] <b>В вашей корзине { $items_amount } товара 🛍</b>
        *[many] <b>В вашей корзине { $items_amount } товаров 🛍</b>
    }

item-main-cart-page-text =
    <b>{ $name }</b>
    ┌ Кол-во: <b>{ $amount }</b>
    ├ Цена за 1 шт: <i>{ $price }₽</i>
    └ Всего: <i>{ $total }₽</i>

items-total-price-text = 💰 <b>Суммарная стоимость товаров:</b> <i>{ $total_price }₽</i>
clean-cart-text = <b>Вы уверены, что хотите полностью очистить корзину?</b>🧹
delete-item-text = <b>Вы уверены, что хотите удалить данный товар из корзины?</b>
change-item-amount-text =
    <b>Для изменения количества товара используй ➖ | ➕</b>

    <i>Не забудь нажать <b>подтвердить</b></i>

old-amount-value-text = Товар уже находится в нужно количестве 😉
item-amount-cart-text =
  <b><i>{$amount ->
        [one]Сейчас в корзине { $amount } позиция
        [few]Сейчас в корзине { $amount } позиции
       *[many]Сейчас в корзине { $amount } позиций
    } данного товара 🛍</i></b>