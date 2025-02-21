#!/bin/sh

echo "Started SHUKACH.SOCIAL pipeline!"

cd /app

# Запуск парсерів
/usr/local/bin/python /app/manage.py run_parsers_telegram
/usr/local/bin/python /app/manage.py run_parsers_telegram_reversed

# Запуск кодування мов
/usr/local/bin/python /app/manage.py run_languagers_text

# Запуск автокодування
/usr/local/bin/python /app/manage.py run_autotaggers_text
