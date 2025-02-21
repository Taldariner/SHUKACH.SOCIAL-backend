import asyncio
import logging

from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramRetryAfter, TelegramAPIError
from django.core.management.base import BaseCommand
from django.db.models import Max
from django.conf import settings

from mailings.models import MailingTelegram
from news.models import NewsPost


logging.basicConfig(level = logging.ERROR)

bot = Bot(token = settings.TELEGRAM_TOKEN)
dp = Dispatcher()


class Command(BaseCommand):
    help = "Send Telegram mailings"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting Telegram mailings..."))
        asyncio.run(send_mailing())
        self.stdout.write(self.style.SUCCESS("Successfully sent Telegram mailings!"))

            
async def send_mailing():
    try:
        mailings_list = await get_mailings_list()

        for mailing in mailings_list:
            mailing_text = await get_mailings_text(mailing)
            try:
                await bot.send_message(mailing.group, mailing_text, parse_mode = "Markdown", disable_web_page_preview = True)
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
            except TelegramAPIError as e:
                print(f"Error sending message to chat {mailing.group}: {e}")
    finally:
        await bot.session.close()


@sync_to_async
def get_mailings_list():
    return list(MailingTelegram.objects.exclude(group__isnull = True).exclude(group__exact = ''))


@sync_to_async
def get_mailings_text(mailing):
    channels = [mailing.news_channel_1, mailing.news_channel_2, mailing.news_channel_3, mailing.news_channel_4, mailing.news_channel_5]
    channels = [channel for channel in channels if channel is not None]

    mailing_text = "Актуальні новини станом на зараз:\n\n"

    for channel in channels:
        news = (
            NewsPost.objects.filter(channel = channel)
            .order_by('-time_posted')
            .first()
        )
        
        if news:
            mailing_text += (
                f"📢 {news.channel.name}:\n\n"
                f"{news.header}... "
                f"[Читати далі]({news.channel.social.tag_template.format(channel_tag = news.channel.tag, post_id = str(news.post_id))}).\n\n"
            )

    return mailing_text
