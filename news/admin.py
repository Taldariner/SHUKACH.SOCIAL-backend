from django.contrib import admin

from news.models import (SocialMedia, Country, NewsChannel, 
						 PostLanguage, PostEntity, PostKeyword, PostHashtag, 
						 NewsPost)


admin.site.register(SocialMedia)
admin.site.register(Country)
admin.site.register(NewsChannel)

admin.site.register(PostLanguage)
admin.site.register(PostEntity)
admin.site.register(PostKeyword)
admin.site.register(PostHashtag)

admin.site.register(NewsPost)
