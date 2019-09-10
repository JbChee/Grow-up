from django.contrib import admin
from goods.models import *


# Register your models here.
@admin.register(TypeInfo)
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ('ttitle',)


@admin.register(GoodsInfo)
class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ('gtitle',)


