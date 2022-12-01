from django.urls import path

from rankstatapp.views import Current_game_Participants, hello_world, ranksearch

app_name = "rankstatapp"

urlpatterns = [
    path('hello_world/',hello_world, name='helloworld'),
    path('home/',hello_world, name='home'),
    path('summoners/',ranksearch, name='summoners'),
    path('current_game/',Current_game_Participants, name='current_game'),

]