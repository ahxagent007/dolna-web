from django.urls import path
from .views import *



urlpatterns=[
    path('driver/registration', DriverRegistration.as_view()),
]