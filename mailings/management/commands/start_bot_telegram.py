import asyncio
import logging

from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher
from aiogram.types import Message, BotCommand
from aiogram.filters.command import Command as TgCommand
from aiogram.exceptions import TelegramRetryAfter, TelegramAPIError
from django.core.management.base import BaseCommand
from django.conf import settings

from mailings.models import MailingTelegram


logging.basicConfig(level = logging.ERROR)

bot = Bot(token = settings.TELEGRAM_TOKEN)
dp = Dispatcher()


class Command(BaseCommand):
    help = "Start Telegram bot"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Telegram bot..."))
        try:
            asyncio.run(start_bot())
        except (KeyboardInterrupt, SystemExit):
            self.stdout.write(self.style.NOTICE("Bot stopped."))


async def start_bot():
    # print("Bot is running!")
    # await set_commands(bot)  
    register_handlers(dp)
    await dp.start_polling(bot)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command = "reg", description = "Реєструє чат для розсилки"),
        BotCommand(command = "unreg", description = "Припиняє реєстрацію"),
    ]
    try:
        await bot.set_my_commands(commands)
        print("Commands set successfully!")
    except TelegramRetryAfter as e:
        print(f"Flood control exceeded. Retry after {e.retry_after} seconds.")
    except TelegramAPIError as e:
        print(f"Error while setting bot commands: {e}")


def register_handlers(dp):
    @dp.message(TgCommand('reg'))
    async def register_chat(message: Message):
        try:
            code  = message.text.split(" ")[1]
            group = str(message.chat.id)
            reg_result = await register_mailing_code(code, group)
            await message.reply(reg_result)
        except Exception as e:
            await message.reply(f"Щоб зареєструвати чат для розсилки, надішліть команду у форматі /reg 'код'.\n\n{e}")

    @dp.message(TgCommand('unreg'))
    async def unregister_chat(message: Message):
        try:
            code  = message.text.split(" ")[1]
            group = str(message.chat.id)
            unreg_result = await unregister_mailing_code(code, group)
            await message.reply(unreg_result)
        except Exception as e:
            await message.reply(f"Не вдалося зняти чат з реєстрації.\n\n{e}")


@sync_to_async
def register_mailing_code(code, group):
    mailing = MailingTelegram.objects.filter(code = code).first()
    if mailing is None:
        return f"""Не знайдено код розсилки {code}.\nПеревірте правильність введеня коду, або створіть розсилку в особистому кабінеті:\nhttps://shukach.pro/accounts/profile/"""
    elif mailing.group is not None:
        return f"""Вибачте, але код розсилки {code} вже прив'язано у іншому чаті.\nПеревірте правильність введеня коду, або створіть розсилку в особистому кабінеті:\nhttps://shukach.pro/accounts/profile/"""
    else:
        mailing.group = group
        mailing.save()
        return f"Чат успішно прив'язано до розсилки за кодом {code}!"


@sync_to_async
def unregister_mailing_code(code, group):
    mailing = MailingTelegram.objects.filter(code = code, group = group).first()
    if mailing is None:
        return f"""Цей чат не прив'язано для розсилки за кодом {code}.\nЗареєструйте чат для розсилки за допомогою команди /reg 'код' або перевірте правильність введеня коду в особистому кабінеті:\nhttps://shukach.pro/accounts/profile/"""
    else:
        mailing.group = None
        mailing.save()
        return f"Чат успішно відв'язано від розсилки за кодом {code}!"
