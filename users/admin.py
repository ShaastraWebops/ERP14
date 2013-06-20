from django.contrib import admin
from users.models import ERPUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = ERPUser

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]

admin.site.register(User, UserProfileAdmin)