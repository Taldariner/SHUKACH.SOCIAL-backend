@echo off

echo Started SHUKACH.SOCIAL pipeline!

:: Нескінченний цикл для запуску команд
:loop

:: Активація віртуального середовища
call .\__venv__\Scripts\activate

:: Запуск парсерів
python manage.py run_parsers_telegram

:: Запуск кодування мов
python manage.py run_languagers_text

:: Запуск автокодування
python manage.py run_autotaggers_text

:: Деактивація віртуального середовища
deactivate

:: Очікування 5 хвилин перед наступним запуском
timeout /t 300 /nobreak

:: Повернення до початку циклу
goto loop
