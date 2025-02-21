from django.db import models
from django_countries.fields import CountryField


class SocialMedia(models.Model):
    name         = models.CharField(max_length = 128)
    tag_template = models.CharField(max_length = 128, null = True, blank = True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name        = models.CharField(max_length = 128)
    alpha2_code = CountryField()

    def __str__(self):
        return self.name


class NewsChannel(models.Model):
    
    class ChannelType(models.TextChoices):
        NONE_TYPE    = "--", "Undefined"
        NEWS_CHANNEL = "NC", "News Channel"
        AUTHORS_BLOG = "AB", "Author's Blog"
        ANONYMOUS    = "AN", "Anonymous Channel"
        OFFICIAL     = "OC", "Official Channel"
        OTHER_TYPE   = "OK", "Other"
    
    channel_type = models.CharField(
        max_length = 2,
        choices    = ChannelType.choices,
        default    = ChannelType.NONE_TYPE,
    )
    name = models.CharField(max_length = 128)
    tag  = models.CharField(max_length = 128, db_index = True)
    
    last_parsed_post  = models.IntegerField(default = 0)
    first_parsed_post = models.IntegerField(default = 0)

    country = models.ForeignKey(Country,     null = True, on_delete = models.SET_NULL)
    social  = models.ForeignKey(SocialMedia, null = True, on_delete = models.SET_NULL)
    
    def __str__(self):
        return f"{self.social.name} - {self.name}"


# Autotaggers data for posts
class PostLanguage(models.Model):
    name = models.CharField(max_length = 2)

    def __str__(self):
        return self.name


class PostEntity(models.Model):
    lemmatized_name = models.CharField(max_length = 128, db_index = True)
    display_name    = models.CharField(max_length = 128, db_index = True)
    entity_type     = models.CharField(max_length = 128)

    def __str__(self):
        return f"{self.display_name} - {self.entity_type}"


class PostKeyword(models.Model):
    name = models.CharField(max_length = 128, db_index = True)

    def __str__(self):
        return self.name


class PostHashtag(models.Model):
    name = models.CharField(max_length = 128, db_index = True)

    def __str__(self):
        return self.name


class NewsPost(models.Model):

    class PostType(models.TextChoices):
        TYPE_NONE  = "--", "Undefined"
        TYPE_TEXT  = "TT", "Text"
        TYPE_VIDEO = "TV", "Video"
        TYPE_OTHER = "TO", "Other"
        
    post_type = models.CharField(
        max_length = 2,
        choices    = PostType.choices,
        default    = PostType.TYPE_NONE
    )

    header     = models.TextField()
    text       = models.TextField()

    channel    = models.ForeignKey(NewsChannel, on_delete = models.CASCADE)
    post_id    = models.IntegerField(default = 0)

    time_posted    = models.DateTimeField()
    time_parsed    = models.DateTimeField()
    time_pipelined = models.DateTimeField(null = True)
    
    pipelined  = models.IntegerField(default = 0)
    language   = models.ForeignKey(PostLanguage, null = True, on_delete = models.SET_NULL)
    entities   = models.ManyToManyField(PostEntity,  blank = True)
    keywords   = models.ManyToManyField(PostKeyword, blank = True)
    hashtags   = models.ManyToManyField(PostHashtag, blank = True)  

    def __str__(self):
        return self.header
