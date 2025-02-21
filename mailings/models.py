from django.db import models

from accounts.models import UserProfile
from news.models import NewsChannel


class MailingTelegram(models.Model):
    user = models.OneToOneField(UserProfile, on_delete = models.CASCADE)
    
    code  = models.CharField(max_length = 8)
    group = models.CharField(max_length = 128, blank = True, null = True)

    news_channel_1 = models.ForeignKey(NewsChannel, on_delete = models.SET_NULL, blank = True, null = True, related_name = "+")
    news_channel_2 = models.ForeignKey(NewsChannel, on_delete = models.SET_NULL, blank = True, null = True, related_name = "+")
    news_channel_3 = models.ForeignKey(NewsChannel, on_delete = models.SET_NULL, blank = True, null = True, related_name = "+")
    news_channel_4 = models.ForeignKey(NewsChannel, on_delete = models.SET_NULL, blank = True, null = True, related_name = "+")
    news_channel_5 = models.ForeignKey(NewsChannel, on_delete = models.SET_NULL, blank = True, null = True, related_name = "+")
    
    def __str__(self):
        return f"{self.user.user.username}'s Telegram mailing"
