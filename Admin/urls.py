from django.urls import path
from .views import *


urlpatterns=[
    path('', Dashboard, name='Dashboard'),
    path('Login', Login, name='Login'),
    path('All_Rider', All_Rider, name='All_Rider'),
    path('Add_Rider',Add_Rider,name= 'Add_Rider'),
    path('Edit_Rider/<rider_id>', Edit_Rider, name='Edit_Rider'),
    path('Delete_Rider/<rider_id>', Delete_Rider, name='Delete_Rider'),

    path('All_Driver', All_Driver, name='All_Driver'),
    path('Add_Driver', Add_Driver, name='Add_Driver'),
    path('Edit_Driver/<driver_id>', Edit_Driver, name='Edit_Driver'),
    path('Delete_Driver/<driver_id>', Delete_Driver, name='Delete_Driver'),

    path('Add_Car/<driver_id>', Add_Car, name='Add_Car'),
    path('Edit_Car/<driver_id>', Edit_Car, name='Edit_Car'),
    path('Delete_Car/<car_id>', Delete_Car, name='Delete_Car'),

]