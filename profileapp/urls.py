from django.contrib import admin
from django.urls import include, path

from profileapp.views import ProfileCreateView

app_name = 'profileapp'

urlpatterns = [
    path('create/', ProfileCreateView.as_view(), name='create'),
]
