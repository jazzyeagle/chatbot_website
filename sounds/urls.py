from django.urls import path
from sounds.views import *

urlpatterns = [
                path('search',                sound_search,  name='sound_search'),
                path('<str:sound_code>',      sound,         name='sound'),
                path('<str:sound_code>/rate', sound_rate,    name='sound_rate'),
                path('',                      sounds,        name='sounds'),
              ]
