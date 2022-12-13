from django.urls import path
from .views import *
from .api import get_car_details


urlpatterns=[
    path('GetCarDetails/<driver_id>', get_car_details, name='get_car_details'),
]