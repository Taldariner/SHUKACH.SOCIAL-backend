import csv
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from news.forms import NewsFilterForm, NewsPostForm
from news.models import NewsPost


class NewsMainView(LoginRequiredMixin, View):
    def get(self, request):

        news_filter_form = NewsFilterForm(request.GET, initial = {'results_per_page': '50',
                                                                  'posted_from':      timezone.now() - timedelta(weeks = 1),
                                                                  'posted_to':        timezone.now()})
        news_filters = Q()

        if news_filter_form.is_valid():
            socials     = news_filter_form.cleaned_data.get('socials')
            countries   = news_filter_form.cleaned_data.get('countries')
            channels    = news_filter_form.cleaned_data.get('channels')

            languages   = news_filter_form.cleaned_data.get('languages')
            entities    = news_filter_form.cleaned_data.get('entities')
            keywords    = news_filter_form.cleaned_data.get('keywords')
            hashtags    = news_filter_form.cleaned_data.get('hashtags')

            posted_from = news_filter_form.cleaned_data.get('posted_from')
            posted_to   = news_filter_form.cleaned_data.get('posted_to')

            if socials:
                socials_filter = Q()
                for social in socials:
                    socials_filter |= Q(channel__social = social)
                news_filters &= socials_filter
            
            if countries:
                countries_filter = Q()
                for country in countries:
                    countries_filter |= Q(channel__country = country)
                news_filters &= countries_filter

            if channels:
                channels_filter = Q()
                for channel in channels:
                    channels_filter |= Q(channel = channel)
                news_filters &= channels_filter

            if languages:
                languages_filter = Q()
                for language in languages:
                    languages_filter |= Q(language = language)
                news_filters &= languages_filter

            if entities:
                entities_filter = Q()
                for entity in entities:
                    entities_filter |= Q(entities = entity)
                news_filters &= entities_filter

            if keywords:
                keywords_filter = Q()
                for keyword in keywords:
                    keywords_filter |= Q(keywords = keyword)
                news_filters &= keywords_filter

            if hashtags:
                hashtags_filter = Q()
                for hashtag in hashtags:
                    hashtags_filter |= Q(hashtags = hashtag)
                news_filters &= hashtags_filter

            if posted_from:
                news_filters &= Q(time_posted__gte = posted_from)
            if posted_to:
                news_filters &= Q(time_posted__lte = posted_to)

            news_list = NewsPost.objects.filter(news_filters).select_related('channel', 'channel__social').order_by('-time_posted')

            results_per_page = news_filter_form.cleaned_data.get('results_per_page', '50')
            paginator = Paginator(news_list, results_per_page)
            page_number = news_filter_form.cleaned_data.get('page', 1)

            try:
                news_page = paginator.page(page_number)
            except PageNotAnInteger:
                news_page = paginator.page(1)
            except EmptyPage:
                news_page = paginator.page(paginator.num_pages)

            context = {
                "news_count":       news_list.count(),
                "news_page":        news_page,
                "news_filter_form": news_filter_form,

                "active_app": "news",
            }

        else:
            context = {
                "news_count":       0,
                "news_page":        None,
                "news_filter_form": news_filter_form,

                "active_app": "news",
            }

        return render(request, "news/news_list.html", context)


class NewsExportView(LoginRequiredMixin, View):
    def get(self, request):
        return self.export_news_csv(request)

    def export_news_csv(self, request):
    
        news_filter_form = NewsFilterForm(request.GET)
        news_filters = Q()

        if news_filter_form.is_valid():
            socials     = news_filter_form.cleaned_data.get('socials')
            countries   = news_filter_form.cleaned_data.get('countries')
            channels    = news_filter_form.cleaned_data.get('channels')

            languages   = news_filter_form.cleaned_data.get('languages')
            entities    = news_filter_form.cleaned_data.get('entities')
            keywords    = news_filter_form.cleaned_data.get('keywords')
            hashtags    = news_filter_form.cleaned_data.get('hashtags')

            posted_from = news_filter_form.cleaned_data.get('posted_from')
            posted_to   = news_filter_form.cleaned_data.get('posted_to')

            if socials:
                socials_filter = Q()
                for social in socials:
                    socials_filter |= Q(channel__social = social)
                news_filters &= socials_filter
            
            if countries:
                countries_filter = Q()
                for country in countries:
                    countries_filter |= Q(channel__country = country)
                news_filters &= countries_filter

            if channels:
                channels_filter = Q()
                for channel in channels:
                    channels_filter |= Q(channel = channel)
                news_filters &= channels_filter

            if languages:
                languages_filter = Q()
                for language in languages:
                    languages_filter |= Q(language = language)
                news_filters &= languages_filter

            if entities:
                entities_filter = Q()
                for entity in entities:
                    entities_filter |= Q(entities = entity)
                news_filters &= entities_filter

            if keywords:
                keywords_filter = Q()
                for keyword in keywords:
                    keywords_filter |= Q(keywords = keyword)
                news_filters &= keywords_filter

            if hashtags:
                hashtags_filter = Q()
                for hashtag in hashtags:
                    hashtags_filter |= Q(hashtags = hashtag)
                news_filters &= hashtags_filter

            if posted_from:
                news_filters &= Q(time_posted__gte = posted_from)
            if posted_to:
                news_filters &= Q(time_posted__lte = posted_to)

        else:
            context = {
                "news_count":       0,
                "news_page":        None,
                "news_filter_form": news_filter_form,

                "active_app": "news",
            }

            return render(request, "news/news_list.html", context)

        news_list = NewsPost.objects.filter(news_filters).select_related('channel', 'channel__social').order_by('-time_posted')

        now = timezone.now().strftime("%d.%m.%Y_%H.%M.%S")
        filename = f"news_{now}.csv"

        response = HttpResponse(content_type = 'text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, delimiter = ';', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        writer.writerow(['ID', 'Social Media', 'Country', 'Channel', 'Time Posted', 'Link', 'Text'])

        for news in news_list:
            writer.writerow([news.id, news.channel.social, news.channel.country, news.channel.name, news.time_posted, f"t.me/{news.channel.tag}/{news.post_id}", news.text])

        return response


class NewsDetailView(LoginRequiredMixin, View):
    def get(self, request, news_id):
        news  = get_object_or_404(NewsPost.objects.prefetch_related('entities', 'keywords', 'hashtags'), pk = news_id)

        context = {
            "news": news, 
            "entities": news.entities.all(),
            "keywords": news.keywords.all(),
            "hashtags": news.hashtags.all(),

            "active_app": "news",
        }
        
        return render(request, "news/news_detail.html", context)


class NewsCreateView(LoginRequiredMixin, View):
    def get(self, request):
        
        if not request.user.userprofile.subscription.editor:
            return HttpResponseForbidden("You are not authorized to create this post.")
        
        form = NewsPostForm()

        context = {
            "form": form,

            "active_app": "news",
        }
        
        return render(request, "news/news_create.html", context)

    def post(self, request):
        
        if not request.user.userprofile.subscription.editor:
            return HttpResponseForbidden("You are not authorized to create this post.")

        form = NewsPostForm(request.POST)

        if form.is_valid():
            news = form.save(commit = False)
            news.time_pipelined = timezone.now()
            news.pipelined = -1
            news.save()
            form.save_m2m()
            
            return redirect('news:detail', news_id = news.id)

        else:
            print("FORM IS NOT VALID!")
            context = {
                "form": form,

                "active_app": "news",
            }
            return render(request, "news/news_create.html", context)


class NewsUpdateView(LoginRequiredMixin, View):
    def get(self, request, news_id):
        
        if not request.user.userprofile.subscription.editor:
            return HttpResponseForbidden("You are not authorized to edit this post.")
        
        news = get_object_or_404(NewsPost.objects.prefetch_related('entities', 'keywords', 'hashtags'), pk = news_id)
        form = NewsPostForm(instance = news)

        context = {
            "news": news,
            "form": form,

            "active_app": "news",
        }
        
        return render(request, "news/news_update.html", context)

    def post(self, request, news_id):
        
        if not request.user.userprofile.subscription.editor:
            return HttpResponseForbidden("You are not authorized to edit this post.")

        news = get_object_or_404(NewsPost.objects.prefetch_related('entities', 'keywords', 'hashtags'), pk = news_id)
        form = NewsPostForm(request.POST, instance = news)

        if form.is_valid():
            form.save(commit = False)
            news.time_pipelined = timezone.now()
            news.pipelined = -1
            news.save()
            form.save_m2m()
            
            return redirect('news:detail', news_id = news.id)

        else:

            context = {
                "news": news,
                "form": form,

                "active_app": "news",
            }

            return render(request, "news/news_update.html", context)


class NewsDeleteView(LoginRequiredMixin, View):
    def get(self, request, news_id):

        if not request.user.userprofile.subscription.editor:
            return HttpResponseForbidden("You are not authorized to delete this post.")

        news  = get_object_or_404(NewsPost.objects.prefetch_related('entities', 'keywords', 'hashtags'), pk = news_id)

        context = {
            "news": news, 
            "entities": news.entities.all(),
            "keywords": news.keywords.all(),
            "hashtags": news.hashtags.all(),

            "active_app": "news",
        }

        return render(request, "news/news_delete.html", context)

    def post(self, request, news_id):
        if not request.user.userprofile.subscription.editor:
            return HttpResponseForbidden("You are not authorized to delete this post.")
        
        news = get_object_or_404(NewsPost, pk = news_id)
        news.delete()

        return redirect('news:main')
