import os
from time import perf_counter
from multiprocessing import Pool

import django
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from news.models import PostEntity, PostKeyword, PostHashtag, NewsPost
from autotaggers.scripts.autotagger_text import pipeline_texts, AUTOTAGGERS_VERSION, SUPPORTED_LANGUAGES


def process_language_texts(language):
    posts_to_autotag = list(NewsPost.objects.filter(pipelined__lt = AUTOTAGGERS_VERSION, language__name = language).order_by('pipelined', '-time_posted')[:25])
    posts_model_name = SUPPORTED_LANGUAGES[language]

    if not posts_to_autotag:
        print(f"No posts found for language: {language}")
        return []

    post_entities, post_keywords, post_hashtags = pipeline_texts([post.text for post in posts_to_autotag], posts_model_name)

    results = []
    for post, entities, keywords, hashtags in zip(posts_to_autotag, post_entities, post_keywords, post_hashtags):
        results.append((post.id, entities, keywords, hashtags))

    return results


def save_language_results(language, results):
    try:
        with transaction.atomic():
            for post_id, entities, keywords, hashtags in results:
                post = NewsPost.objects.get(id = post_id)

                post.time_pipelined = timezone.now()
                post.pipelined = AUTOTAGGERS_VERSION

                post.entities.clear()
                post.keywords.clear()
                post.hashtags.clear()

                for entity_name, entity_type in entities:
                    entity, created = PostEntity.objects.get_or_create(
                        lemmatized_name = entity_name,
                        defaults        = {'display_name': entity_name, 
                                           'entity_type':  entity_type}
                    )
                    post.entities.add(entity)

                for keyword in keywords:
                    keyword_obj, created = PostKeyword.objects.get_or_create(name = keyword[0])
                    post.keywords.add(keyword_obj)

                for hashtag in hashtags:
                    hashtag_obj, created = PostHashtag.objects.get_or_create(name = hashtag)
                    post.hashtags.add(hashtag_obj)

                post.save()
                # print(f"Saved post: {post.id}")

    except Exception as e:
        print(f"Error saving results for language {language}: {e}")


class Command(BaseCommand):
    help = 'Runs autotagger pipeline for some amount of texts, v. 0.2'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING(f"Started texts autotagging {timezone.now()}"))
        ts = perf_counter()

        with Pool(processes = len(SUPPORTED_LANGUAGES)) as pool:
            all_results = pool.map(process_language_texts, SUPPORTED_LANGUAGES.keys())

        for language, results in zip(SUPPORTED_LANGUAGES.keys(), all_results):
            save_language_results(language, results)

        total_processed = sum(len(results) for results in all_results)
        tf = perf_counter()
        self.stdout.write(self.style.SUCCESS(f"Successfully autotagged {total_processed} texts in {(tf - ts):.0f} seconds"))
