#!/bin/bash

echo "Started SHUKACH.SOCIAL pipeline!"

# Нескінченний цикл для запуску команд
while :; do

    # Активація віртуального середовища
    source ./.venv/bin/activate

    # Запуск парсерів
    python3 manage.py run_parsers_telegram

    # Запуск кодування мов
    python3 manage.py run_languagers_text

    # Запуск автокодування
    python3 manage.py run_autotaggers_text

    # Деактивація віртуального середовища
    deactivate

    # Очікування 5 хвилин перед наступним запуском
    sleep 5m

# Повернення до початку циклу 
done
