-brand_name = <b>SneakerStreet</b>

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
