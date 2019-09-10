from django.contrib import admin
from users.models import *

# Register your models here.

@admin.register(UserInfo)
class UserAdmin(admin.ModelAdmin):
    list_display = ( 'uname', 'upw', 'create_time')
    ordering = ('create_time',)


@admin.register(UserAddressInfo)
class UserAddInfoAdmin(admin.ModelAdmin):
    list_display = ('uname',)
