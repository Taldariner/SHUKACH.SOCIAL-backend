import time
import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from news.models import NewsChannel, NewsPost
from parsers.scripts.parser_telegram import parse_telegram_channel


class Command(BaseCommand):
    help = 'Runs the Telegram incremental parser script'

    def handle(self, *args, **kwargs):
        # TODO Implement some proper filtering of appropriate text posts here
        channels_to_parse = NewsChannel.objects.filter(social = 1) # Telegram
        
        self.stdout.write(self.style.WARNING(f"Started Telegram incrementail parsing at {datetime.datetime.now()}"))
        ts = time.perf_counter()

        for channel in channels_to_parse:
            try:
                channel_tag      = channel.tag
                last_parsed_post = channel.last_parsed_post

                parsed_messages, new_min_id, new_max_id = parse_telegram_channel(channel_tag, last_parsed_post, limit = 25)

                with transaction.atomic():

                    for post_data in parsed_messages:
                        news_post = NewsPost(
                            header      = post_data['text'].split('\n')[0],
                            text        = post_data['text'],

                            channel     = channel,
                            post_id     = post_data['post_id'],

                            time_posted = post_data['time_posted'],
                            time_parsed = post_data['time_parsed'],
                        )
                        news_post.save()
                
                    channel.last_parsed_post = new_max_id
                    if channel.first_parsed_post == 0:
                        channel.first_parsed_post = new_min_id
                    channel.save()
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Can't parse channel {channel} for this reason:\n {e}"))

            print(f"{new_min_id:>6} - {new_max_id:>6} - {channel.name}")

        tf = time.perf_counter()
        self.stdout.write(self.style.SUCCESS(f"Successfully parsed {len(channels_to_parse)} channels in {(tf - ts):.0f} seconds"))
