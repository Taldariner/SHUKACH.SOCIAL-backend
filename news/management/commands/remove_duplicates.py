from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count

from news.models import NewsPost


class Command(BaseCommand):
    help = 'Remove duplicate entries from NewsPost table'

    def handle(self, *args, **kwargs):
        duplicates = (
            NewsPost.objects.values('channel', 'time_posted')
            .annotate(count = Count('id'))
            .filter(count__gt = 1)
        )

        self.stdout.write(self.style.SUCCESS(f"Duplicate entries found: {len(duplicates)}"))

        with transaction.atomic():
            for duplicate in duplicates:
                duplicate_posts = (
                    NewsPost.objects.filter(channel    = duplicate['channel'], 
                                            time_posted = duplicate['time_posted'])
                    .order_by('time_parsed')
                )

                for i, post in enumerate(duplicate_posts):
                    if i == 0:
                        continue  # Skip the oldest one
                    self.stdout.write(self.style.WARNING(f"Deleting post with ID: {post.id} and timeparsed: {post.time_parsed} and timeposted {post.time_posted}"))
                    post.delete()

        self.stdout.write(self.style.SUCCESS('Successfully removed duplicate entries'))
