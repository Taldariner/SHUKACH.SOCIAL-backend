from django import forms

from mailings.models import MailingTelegram


class MailingForm(forms.ModelForm):
    class Meta:
        model = MailingTelegram
        fields = [
            'news_channel_1', 
            'news_channel_2', 
            'news_channel_3',
            'news_channel_4',
            'news_channel_5',
        ]

        widgets = {
            'news_channel_1': forms.Select(attrs = {'class': 'form-control mb-3'}),
            'news_channel_2': forms.Select(attrs = {'class': 'form-control mb-3'}),
            'news_channel_3': forms.Select(attrs = {'class': 'form-control mb-3'}),
            'news_channel_4': forms.Select(attrs = {'class': 'form-control mb-3'}),
            'news_channel_5': forms.Select(attrs = {'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set custom empty label for each select field
        self.fields['news_channel_1'].empty_label = "Choose channel to retrieve news from"
        self.fields['news_channel_2'].empty_label = "Choose channel to retrieve news from"
        self.fields['news_channel_3'].empty_label = "Choose channel to retrieve news from"
        self.fields['news_channel_4'].empty_label = "Choose channel to retrieve news from"
        self.fields['news_channel_5'].empty_label = "Choose channel to retrieve news from"
