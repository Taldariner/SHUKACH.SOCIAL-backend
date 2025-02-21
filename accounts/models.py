from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from news.models import (SocialMedia, Country, NewsChannel, 
                         PostLanguage, PostEntity, PostKeyword, PostHashtag)


class Subscription(models.Model):
    name   = models.CharField(max_length = 128)
    price  = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    editor = models.BooleanField(default = False)
    admin  = models.BooleanField(default = False)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    
    subscription_end = models.DateField(default = timezone.now)
    account_balance  = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    subscription     = models.ForeignKey(Subscription, null = True, on_delete = models.SET_NULL)
    
    def __str__(self):
        return self.user.username


class Project(models.Model):
    name = models.CharField(max_length = 128)
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)

    socials   = models.ManyToManyField(SocialMedia,  blank = True)
    countries = models.ManyToManyField(Country,      blank = True)
    channels  = models.ManyToManyField(NewsChannel,  blank = True)
    
    languages = models.ManyToManyField(PostLanguage, blank = True)
    entities  = models.ManyToManyField(PostEntity,   blank = True)
    keywords  = models.ManyToManyField(PostKeyword,  blank = True)
    hashtags  = models.ManyToManyField(PostHashtag,  blank = True)
    
    def __str__(self):
        return self.name
