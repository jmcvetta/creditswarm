# Copyright (c) 2012 Jason McVetta.

from django.contrib import admin

from profile.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'family_name', 'given_name']

admin.site.register(UserProfile, UserProfileAdmin)