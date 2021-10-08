from django.urls import path
from mainsite.views import *

urlpatterns = [
                path('',                      index, name='homepage'),
                path('tours',                 tours, name='tours'),
                path('venues',                venues, name='venues'),
                path('songs',                 songs,  name='songs'),
                path('Sorry For Monologging', tour,  name='tour'),
                path('Sorry For Monologging/Fountain Of Shadows', venue, name='venue'),
                path('Sorry For Monologging/Fountain Of Shadows/Fuel on the Fire', song, name='song')
              ]
