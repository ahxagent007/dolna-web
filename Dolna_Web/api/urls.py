from django.urls import path
from .api import *


urlpatterns=[
    path('Car/Get/Details/<driver_id>', get_car_details, name='get_car_details'),
    path('Rider/Get/Details/<fb_uid>', get_rider_details, name='get_rider_details'),
    path('Driver/Get/Details/<fb_uid>', get_driver_details, name='get_driver_details'),
    path('Rider/Create', create_rider, name='create_rider'),
    path('Driver/Delete/<fb_uid>', delete_driver_details, name='delete_driver_details'),
    path('Rider/Delete/<fb_uid>', delete_rider_details, name='delete_rider_details'),
    path('Driver/Update', driver_update, name='delete_driver_details'),
    path('Rider/Update', rider_update, name='delete_driver_details'),
]