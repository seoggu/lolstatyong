from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from accountapp.views import AccountCreateView, hello_world2

app_name = 'accountapp'

urlpatterns = [
    path('helloworld2/',hello_world2, name='helloworld2'),
    
    path('login/',LoginView.as_view(template_name = 'accountapp/login.html'), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    
    path('create/',AccountCreateView.as_view(), name='create'),
]
