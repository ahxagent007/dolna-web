from django.urls import path
from .views import *


urlpatterns=[
    path('', StartRent, name='StartRent'),
    path('Car/Create', CarCreate.as_view(), name='CarCreate'),
    path('Car/Details/<str:id>', CarDetails.as_view(), name='CarDetails'),
    path('Car/Update/<str:id>', CarUpdate.as_view(), name='CarUpdate')

]