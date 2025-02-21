from django.contrib import admin

from accounts.models import Subscription, UserProfile, Project


admin.site.register(Subscription)
admin.site.register(UserProfile)
admin.site.register(Project)
