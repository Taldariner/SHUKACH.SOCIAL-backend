from django import forms
from django.utils.datastructures import MultiValueDict

from news.models import NewsPost
from accounts.models import Project
from shukach_social.widgets import TagSelectMultiple


class NewsFilterForm(forms.ModelForm):
    posted_from      = forms.DateTimeField(
                            required = False,
                            input_formats = ["%Y-%m-%dT%H:%M"],
                            widget = forms.widgets.DateTimeInput(attrs = {'type': 'datetime-local', 'class': 'form-control'}), 
                        )
    posted_to        = forms.DateTimeField(
                            required = False,
                            input_formats = ["%Y-%m-%dT%H:%M"],
                            widget = forms.widgets.DateTimeInput(attrs = {'type': 'datetime-local', 'class': 'form-control'}),
                        )
    results_per_page = forms.CharField(
                            required = False, initial = '50', 
                            widget = forms.widgets.Select(
                                choices = [('25', '25'), ('50', '50'), ('100', '100')],
                                attrs = {'class': 'form-select custom-select-list-group d-block w-100'}
                            )
                        )
    page             = forms.IntegerField(required = False, initial = 1)

    class Meta:
        model = Project
        
        fields = [
            'socials', 
            'countries', 
            'channels',
            
            'languages',
            'entities', 
            'keywords', 
            'hashtags',
        ]
        
        widgets = {
            'socials':   TagSelectMultiple(attrs = {'class': 'my-3'}), 
            'countries': TagSelectMultiple(attrs = {'class': 'my-3'}), 
            'channels':  TagSelectMultiple(attrs = {'class': 'my-3'}),
            
            'languages': TagSelectMultiple(attrs = {'class': 'my-3'}),
            'entities':  TagSelectMultiple(tags_color = 'bg-primary', attrs = {'class': 'my-3'}), 
            'keywords':  TagSelectMultiple(tags_color = 'bg-success', attrs = {'class': 'my-3'}), 
            'hashtags':  TagSelectMultiple(tags_color = 'bg-warning', attrs = {'class': 'my-3'}),
        }

    def __init__(self, data, **kwargs):
        initial = kwargs.get('initial', {})
        data = MultiValueDict({**{k: [v] for k, v in initial.items()}, **data})
        super().__init__(data, **kwargs)

    def clean_results_per_page(self):
        if self['results_per_page'].html_name not in self.data:
            return '50'
        value = self.cleaned_data.get('results_per_page')
        if value not in ['25', '50', '100']:
            return '50'
        return value


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        
        fields = [
            'post_type',
            'header',
            'text',

            'channel',
            'post_id',
            
            'time_posted',
            'time_parsed',

            'language',
            'entities',
            'keywords',
            'hashtags',
        ]

        widgets = {
            'post_type': forms.Select(attrs = {'class': 'form-select my-3'}),
            'header':    forms.Textarea(attrs = {'class': 'form-control my-3', 'rows': 4}),
            'text':      forms.Textarea(attrs = {'class': 'form-control my-3', 'rows': 8}),
            
            'channel': forms.Select(attrs = {'class': 'form-select my-3'}),
            'post_id': forms.NumberInput(attrs = {'class': 'form-control my-3'}),

            'time_posted': forms.DateTimeInput(attrs = {'class': 'form-control my-3', 'type': 'datetime-local'}),
            'time_parsed': forms.DateTimeInput(attrs = {'class': 'form-control my-3', 'type': 'datetime-local'}),

            'language':  forms.Select(attrs = {'class': 'form-control my-3'}),
            'entities':  TagSelectMultiple(tags_color = 'bg-primary', attrs = {'class': 'my-3'}),
            'keywords':  TagSelectMultiple(tags_color = 'bg-success', attrs = {'class': 'my-3'}),
            'hashtags':  TagSelectMultiple(tags_color = 'bg-warning', attrs = {'class': 'my-3'}),
        }
