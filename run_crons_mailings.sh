#!/bin/sh

echo "Started SHUKACH.SOCIAL mailings!"

cd /app

# Запуск розсилок
/usr/local/bin/python /app/manage.py send_mailings_telegram

