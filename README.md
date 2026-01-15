# FinamRestPy

FinamRestPy - библиотека-обертка над Finam Trade API (REST API) (https://tradeapi.finam.ru/).
Основная цель библиотеки - обеспечить подключение Finam Trade API к коду на Python так,
чтобы ее функции по содержанию были похожи на оригинальные запросы Finam REST API, а у 
разработчиков не было необходимости разбираться в особенностях работы библиотеки.

### Возможности библиотеки

- Подключение к API, автоматическое обновление токена в отдельном потоке
- Выполнение запросов к API и получение ответов
- работа через типы Python

## Установка

_В разработке_

## Использование

Для начала работы необходимо инициализировать модуль:

```python
from finam_rest_py import Finam

finam = Finam('your_finam_token', 'your_account_id')
```

Инструкция, как получить токен и узнать ID аккаунта(-ов), 
есть на сайте Finam Trade API (https://tradeapi.finam.ru/docs/about/)

Для смены аккаунта используйте следующий код, подставив в него ID нужного аккаунта:

```python
from finam_rest_py import Finam

finam = Finam('your_finam_token', 'your_account_id')
finam.set_account('your_other_account_id')
```

Ниже представлен пример запроса для получения информации об аккаунте:

```python
from finam_rest_py import Finam

finam = Finam('your_finam_token', 'your_account_id')
finam.account.get_account()
```


Больше примеров использования можно увидеть в папке examples