from django.urls import path
from mainsite.views import *

urlpatterns = [
                path('',                                                      index,       name='homepage'),
                path('tours',                                                 tours,       name='tours'),
                path('venues',                                                venues,      name='venues'),
                path('songs',                                                 songs,       name='songs'),
                path('<str:tour_name>',                                       tour,        name='tour'),
                path('<str:tour_name>/<str:venue_name>',                      venue,       name='venue'),
                path('<str:tour_name>/<str:venue_name>/<str:song_name>',      song,        name='song'),
                path('<str:tour_name>/<str:venue_name>/<str:song_name>/rate', song_rate,   name='song_rate')
              ]
