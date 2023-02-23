# Проект парсинга pep

## Парсинг документов PEP
Парсер собирает данные обо всех PEP документах, сравнивает статусы и записывает их в файл, также реализованы сбор информации о статусе версий, скачивание архива с документацией и сбор ссылок о новостях в Python, логирует свою работу и ошибки в командную строку и файл логов.

## Технологии проекта
Python — высокоуровневый язык программирования.
BeautifulSoup4 - библиотека для парсинга.
Prettytable - библиотека для удобного отображения табличных данных.

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
<blockquote>git clone git@github.com:numinga27/bs4_parser_pep.git</blockquote>

cd bs4_parser_pep
Cоздать и активировать виртуальное окружение:
<blockquote> python -m venv venv
. venv/scripts/activate
pip install -r requirements.txt</blockquote>

## Примеры команд:

Выведет справку по использованию

<blockquote>python main.py pep -h</blockquote>
Создаст csv файл с таблицей из двух колонок: «Статус» и «Количество»:

<blockquote>python main.py pep -o file</blockquote>
Выводит таблицу prettytable с тремя колонками: "Ссылка на документацию", "Версия", "Статус":

<blockquote>python main.py latest-versions -o pretty </blockquote>
Выводит ссылки в консоль на нововведения в python:

<blockquote>python main.py whats-new</blockquote>

## Автор:
Крылов Андрей тг: @numinga92
