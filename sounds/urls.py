from django.urls import path
from sounds.views import *

urlpatterns = [
                path('',                sounds,        name='sounds'),
                path('<str:sound_code', sound,         name='sound'),
                path('search',          search_sounds, name='search_sounds')
              ]
