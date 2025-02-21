from django.shortcuts import render
from django.views import View
from django.db.models import Max

from news.models import NewsPost


class IndexView(View):
    def get(self, request):
        resonant_channels = ["ukrpravda_news", "truexanewsua", "voynareal", "insiderUKR", "V_Zelenskiy_official"]

        latest_resonant_news = (
            NewsPost.objects.filter(channel__tag__in = resonant_channels)
            .values('channel__tag')
            .annotate(latest_time = Max('time_posted'))
        )

        news_ids = NewsPost.objects.filter(
            channel__tag__in = resonant_channels,
            time_posted__in = [news['latest_time'] for news in latest_resonant_news]
        ).values_list('id', flat = True)

        resonant_news = (
            NewsPost.objects.filter(id__in = news_ids)
            .select_related('channel')
            .order_by('channel__tag', '-time_posted')
        )

        context = {"resonant_news": resonant_news}

        return render(request, "shukach_social/index.html", context)