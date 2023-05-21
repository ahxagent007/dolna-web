from django.urls import path
from .api import *
from .views import *


urlpatterns=[
    path('Car/Get/Details/<driver_id>', get_car_details, name='get_car_details'),
    path('Rider/Get/Details/<fb_uid>', get_rider_details, name='get_rider_details'),
    path('Driver/Get/Details/<fb_uid>', get_driver_details, name='get_driver_details'),
    path('Car/Create', create_car, name='create_car'),
    path('Driver/Create', create_driver, name='create_driver'),
    path('Rider/Create', create_rider, name='create_rider'),
    path('Driver/Delete/<fb_uid>', delete_driver_details, name='delete_driver_details'),
    path('Rider/Delete/<fb_uid>', delete_rider_details, name='delete_rider_details'),
    path('Car/Update/<id>', car_update, name='car_update'),
    path('Driver/Update/<id>', driver_update, name='driver_update'),
    path('Rider/Update/<id>', rider_update, name='delete_driver_details'),
    path('otp/token', OTPToken.as_view(), name='otp-token'),
    path('otp', OTPSend.as_view(), name='otp'),
    path('otp/verify', OTPVerify.as_view(), name='otp-verify')
]
