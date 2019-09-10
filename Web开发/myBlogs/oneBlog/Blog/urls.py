from django.conf.urls import url
from django.contrib import admin
from Blog.views import *


urlpatterns = [
    url(r'^$', index),
]