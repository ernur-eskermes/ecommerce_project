<h2 align="center">Django E-commerce</h2>

Онлайн магазин на Django.

Функции: 

  - Просмотр продуктов.
  - Добавление в корзину, в список желаний.
  - Покупка товаров.
  - Регистрация, авторизация, отправка email с подтверждением.
  - Интернационализация
  - Подписка на рассылку
  
Настройка
------------

Откройте файл settings.py в папке config. И измените в EMAIL_HOST_USER и в EMAIL_HOST_PASSWORD на email и пароль от вашей почты. 

Затем создайте свой Braintree аккаунт для тестовой оплаты товаров и измените BRAINTREE_MERCHANT_ID, BRAINTREE_PUBLIC_KEY, BRAINTREE_PRIVATE_KEY на свои данные. https://www.braintreepayments.com/sandbox

Локальный запуск проекта
------------
```shell
    docker-compose build
    docker-compose up
```
