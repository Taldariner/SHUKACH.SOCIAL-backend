from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from django.views import View

from accounts.forms import ProjectForm
from accounts.models import Project
from mailings.models import MailingTelegram
from mailings.forms import MailingForm


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('accounts:profile')

        return render(request, 'registration/register.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        mailing = MailingTelegram.objects.filter(user = request.user.userprofile).first()
        projects_list  = Project.objects.filter(user = request.user.userprofile)

        context = {
            "mailing":         mailing,
            "projects_list":   projects_list,

            "active_app":      "accounts",
        }
        return render(request, "accounts/profile.html", context)


class MailingCreateView(LoginRequiredMixin, View):
    def post(self, request):
        mailing_code = str(abs(hash(request.user.username)))[:8]
        
        mailing = MailingTelegram(user = request.user.userprofile, code = mailing_code)
        mailing.save()

        return redirect(reverse("accounts:profile"))


class MailingDetailView(LoginRequiredMixin, View):
    def get(self, request, mailing_id):
        mailing = get_object_or_404(MailingTelegram, pk = mailing_id)
        
        if mailing.user != request.user.userprofile:
            raise PermissionDenied
        
        form = MailingForm(instance = mailing)
        context = {
            "mailing":         mailing,
            "form":            form,

            "active_app":      "accounts",
        }

        return render(request, "accounts/mailing_detail.html", context)


class MailingUpdateView(LoginRequiredMixin, View):
    def post(self, request, mailing_id):
        mailing = get_object_or_404(MailingTelegram, pk = mailing_id)
        
        if mailing.user != request.user.userprofile:
            return redirect('accounts:profile')
        
        form = MailingForm(request.POST, instance = mailing)
        
        if not form.is_valid():
            context = {
                "mailing":         mailing,
                "form":            form,

                "active_app":      "accounts",
            }
            return render(request, "accounts/mailing_detail.html", context)
        
        form.save()
        
        return redirect('accounts:mailing_detail', mailing_id = mailing_id)


class ProjectCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return self.post(request)
    
    def post(self, request):
        with transaction.atomic():
            project = Project.objects.create(
                user = request.user.userprofile,
                name = "_",
            )
            project.name = f"Project {project.id}"
            project.save()

        return redirect(reverse("accounts:project_detail", args = [project.id]))
        

class ProjectDetailView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        project   = get_object_or_404(Project, pk = project_id)
        
        if project.user != request.user.userprofile:
            raise PermissionDenied

        form = ProjectForm(instance = project)
        context = {
            "project":    project,
            "form":       form,

            "active_app": "accounts",
        }

        return render(request, "accounts/project_detail.html", context)


class ProjectUpdateView(LoginRequiredMixin, View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, pk = project_id)
        if project.user != request.user.userprofile:
            return redirect('accounts:profile')
        else:
            
            form = ProjectForm(request.POST, instance = project)
            if form.is_valid():
                form.save(commit = False)
                project.save()
                form.save_m2m()
                return redirect('accounts:project_detail', project_id = project_id)
            else:
                context = {
                    "project": project,
                    "form":    form,

                    "active_app": "news",
                }
                return render(request, "accounts/project_detail.html", context)


class ProjectDeleteView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        project = get_object_or_404(Project, pk = project_id)
        if project.user != request.user.userprofile:
            raise PermissionDenied

        context = {
            "project":  project,

            "saved_socials":   project.socials.all,
            "saved_countries": project.countries.all,
            "saved_channels":  project.channels.all,
            
            "saved_languages": project.languages.all,
            "saved_entities":  project.entities.all,
            "saved_keywords":  project.keywords.all,
            "saved_hashtags":  project.hashtags.all,

            "active_app":      "accounts",
        }

        return render(request, "accounts/project_delete.html", context)

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk = project_id)
        if project.user != request.user.userprofile:
            return redirect('accounts:profile')
        else:
            project.delete()
            return redirect('accounts:profile')


class ProjectSearchView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        project = get_object_or_404(Project, pk = project_id)
        if project.user != request.user.userprofile:
            return redirect('accounts:profile')
        else:
            socials   = list(project.socials.values_list('pk',   flat = True))
            countries = list(project.countries.values_list('pk', flat = True))
            channels  = list(project.channels.values_list('pk',  flat = True))
            
            languages = list(project.languages.values_list('pk', flat = True))
            entities  = list(project.entities.values_list('pk',  flat = True))
            keywords  = list(project.keywords.values_list('pk',  flat = True))
            hashtags  = list(project.hashtags.values_list('pk',  flat = True))

            query_params = {
                'socials':   socials,
                'countries': countries,
                'channels':  channels,

                'languages': languages,
                'entities':  entities,
                'keywords':  keywords,
                'hashtags':  hashtags,

                'results_per_page': '50',
                'page': '1',
                'posted_from': (timezone.now() - timedelta(days = 7)).strftime("%Y-%m-%dT%H:%M"),
                'posted_to':   timezone.now().strftime("%Y-%m-%dT%H:%M"),
            }

            query_string = urlencode(query_params, doseq = True)
            redirect_url = f"{reverse('news:main')}?{query_string}"
            
            return HttpResponseRedirect(redirect_url)
