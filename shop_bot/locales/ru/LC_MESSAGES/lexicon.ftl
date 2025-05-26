-brand_name = <b>НАЗВАНИЕ МАГАЗИНА</b>

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
faq-text = <b>Здесь ты найдешь ответы на часто задаваемые вопросы</b> 🗨
question-answer =
    <b>{ $question }</b>

    { $answer }

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

# delivery dialog
input-name-text = <b>Введите ФИО</b> 🙋
input-number-text = <b>Введите ваш номер телефона</b> <i>(В формате: 7*********)</i>
input-city-text = <b>Введите название города</b> 🏙
input-street-text = <b>Введите название улицы</b> 🚚
input-house-text = <b>Введите номер дома</b> 🏠
input-flat-text = <b>Введите номер квартиры</b> <i>(если дом частный введите "-")</i>
confirmation-delivery-data = <b>Подтверждаете данные доставки?</b> 👇

delivery-name = <b>ФИО</b>: <i>{ $name }</i>
delivery-number = <b>Номер телефона</b>: <i>{ $number }</i>
delivery-city = <b>Город</b>: <i>{ $city }</i>
delivery-street = <b>Улица</b>: <i>{ $street }</i>
delivery-house = <b>Дом</b>: <i>{ $house }</i>
delivery-flat = <b>Квартира</b>: <i>{ $flat }</i>

incorrect-text-input =
    Некорректный ввод ❌
    Повторите попытку 🔁

payment-text = <b>Осталось совсем немного 🤏</b>
how-to-pay-text = Используйте кнопку  выше для оплаты ⬆