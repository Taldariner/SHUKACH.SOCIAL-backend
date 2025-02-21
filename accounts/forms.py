from django import forms

from shukach_social.widgets import TagSelectMultiple
from accounts.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',

            'socials', 
            'countries', 
            'channels',

            'languages',
            'entities', 
            'keywords', 
            'hashtags',
        ]

        widgets = {
            'name':      forms.TextInput(attrs = {'class': 'form-control form-main mb-3 text-primary fs-1-5', 
                                                  'placeholder': 'Project name'}),


            'socials':   TagSelectMultiple(attrs = {'class': 'mb-3'}), 
            'countries': TagSelectMultiple(attrs = {'class': 'mb-3'}), 
            'channels':  TagSelectMultiple(attrs = {'class': 'mb-3'}),

            'languages': TagSelectMultiple(attrs = {'class': 'mb-3'}),
            'entities':  TagSelectMultiple(tags_color = 'bg-primary', attrs = {'class': 'mb-3'}), 
            'keywords':  TagSelectMultiple(tags_color = 'bg-success', attrs = {'class': 'mb-3'}), 
            'hashtags':  TagSelectMultiple(tags_color = 'bg-warning', attrs = {'class': 'mb-3'}),
        }

        labels = {
            'name':      "",

            'socials':   "", 
            'countries': "", 
            'channels':  "",

            'languages': "",
            'entities':  "", 
            'keywords':  "", 
            'hashtags':  "",
        }
