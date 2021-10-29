from django.urls import path
from users.views import *


urlpatterns = [
                path('',               users, name='users'),
                path('<str:username>', user,  name='user')
              ]
