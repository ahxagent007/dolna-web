from django.urls import path
from .views import *


urlpatterns=[
    path('', home, name='Home'),
    path('About', About, name='About'),
    path('Contact', Contact, name='Contact'),
]