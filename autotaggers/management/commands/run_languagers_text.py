from time import perf_counter

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from autotaggers.scripts.languager_text import identify_lang
from news.models import NewsPost, PostLanguage


class Command(BaseCommand):
    help = 'Runs language indentification for some amount of texts, v. 0.2'

    def handle(self, *args, **kwargs):
        posts_to_languify = NewsPost.objects.filter(language__isnull = True).order_by('-time_posted')[:100]
        
        self.stdout.write(self.style.WARNING(f"Started texts language indentification {timezone.now()}"))
        ts = perf_counter()

        for post in posts_to_languify:
            
            post_text = post.text
            post_lang = identify_lang(post_text)

            with transaction.atomic():
                
                if post_lang:
                    language, created = PostLanguage.objects.get_or_create(
                        name = post_lang,
                    )
                    
                    post.language = language
                
                post.save()

        tf = perf_counter()
        self.stdout.write(self.style.SUCCESS(f"Successfully identified language for {posts_to_languify.count()} texts in {(tf - ts):.0f} seconds"))
