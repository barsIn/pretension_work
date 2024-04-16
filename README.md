# Проект По учету договоров и претензионной работы: 
[Pretension work](https://github.com/barsIn/pretension_work)

<br>

## Оглавление:
- [Технологии](#технологии)
- [Установка и запуск](#установка-и-запуск)
- [Описание работы](#описание-работы)
- [Автор](#автор)

<br>

## Технологии:

<details><summary>Подробнее</summary>

**Языки программирования, библиотеки и модули:**

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?logo=python)](https://www.python.org/)

**Фреймворк, расширения и библиотеки:**

[![Django](https://img.shields.io/badge/Django-v4.2.1-blue?logo=Django)](https://www.djangoproject.com/)


**Базы данных и инструменты работы с БД:**

[![SQLite3](https://img.shields.io/badge/-SQLite3-464646?logo=SQLite)](https://www.sqlite.com/version3.html)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)

[⬆️Оглавление](#оглавление)
</details>

<br>

## Установка и запуск:
Удобно использовать принцип copy-paste - копировать команды из GitHub Readme и вставлять в командную строку Git Bash или IDE.

<details><summary>Локальный запуск</summary> 


1. Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, но их можно оставить):
```bash
git clone https://github.com/barsIn/pretension_work.git
touch .env
```
<details><summary>Локальный запуск: Django/SQLite3</summary>

2. Создайте и активируйте виртуальное окружение:
   * Если у вас Linux/macOS
   ```bash
    python3 -m venv venv && source venv/bin/activate
   ```
   * Если у вас Windows
   ```bash
    python -m venv venv && source venv/Scripts/activate
   ```

3. Установите в виртуальное окружение все необходимые зависимости из файла **requirements.txt**:
```bash
python -m pip install --upgrade pip && pip install -r requirements.txt
```

4. Выполните миграции, загрузку данных, создание суперюзера и запустите приложение:
```bash
python tree_menu/manage.py makemigrations && \
python tree_menu/manage.py migrate && \
python tree_menu/manage.py load_data && \
python tree_menu/manage.py create_superuser && \
python tree_menu/manage.py runserver
```
Сервер запустится локально по адресу `http://127.0.0.1:8000/`

5. Остановить приложение можно комбинацией клавиш Ctl-C.
<h1></h1>
 </details>

<h1></h1></details>


[⬆️Оглавление](#оглавление)

<br>

## Описание работы:

Данный сервис преднозначен для учета договоров на поставку ТМЦ и расчета неустойки за срыв сроков поставки и оплаты.
Для работы необходимо сперва создать поставщиков (*реализован как ввод через форму, так и массовый ввод через excel файл*), создать работников и отделы.
После выполнения данных шагов можно приступать к заведению договоров. Неустойка расчитывается автоматически. *В дальнейшем будет реализован расчет ежедневно в полночь при помощи Celery*
При отображении договора выводится так же информация о выполненных поставках и оплатах *их так же можно массово вводить из Excel*
Так же при выборе контрагента высвечивается информация по непоставленным договорам и неоплаченным поставкам.
Дайльнейший функцианал еще в работе.


[⬆️Оглавление](#оглавление)

<br>

## Автор:
[Gerasimov Igor](https://github.com/barsIn)

[⬆️В начало](#Проект)
