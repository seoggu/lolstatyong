from django.contrib import admin
from django.urls import path

from rankstatapp.views import hello_world, rankinfo, ranksearch

app_name = "rankstatapp"

urlpatterns = [
    path('hello_world/',hello_world, name='helloworld'),
    path('summoners/',ranksearch, name='summoners'),
    path('rankinfo/',rankinfo, name='rankinfo'),
]