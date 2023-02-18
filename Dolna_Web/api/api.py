from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from Rent.models import Car
from Rent.serializer import CarSerializer
from User.models import Rider, Driver
from User.serializer import RiderSerializer, DriverSerializer
import json


@api_view(['GET'])
def get_car_details(request, driver_id):

    try:
        car = Car.objects.get(ID=driver_id)
        data = CarSerializer(car, many=False).data

        return Response(data)
    except:
        return Response({})


@api_view(['GET'])
def get_rider_details(request, fb_uid):

    try:
        rider = Rider.objects.get(FirebaseID=fb_uid)
        data = RiderSerializer(rider, many=False).data

        return Response(data)
    except:
        return Response({})


@api_view(['GET'])
def get_driver_details(request, fb_uid):

    try:
        driver = Driver.objects.get(FirebaseID=fb_uid)
        data = DriverSerializer(driver, many=False).data

        return Response(data)
    except:
        return Response({})


@api_view(['POST'])
def create_car(request):

    try:

        serializer = CarSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
                'Message' : 'Car Details added Successfully'
            })

    except Exception as e:
        return Response(
            {
                'msg': 'Wrong Information or Format',
                'Error': str(e)
            }
        )


@api_view(['POST'])
def create_driver(request):

    try :
        serializer = DriverSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    except Exception as e:
        return Response(
            {
                'msg': 'Wrong Information or Format',
                'Error': str(e)
            }
        )


@api_view(['POST'])
def create_rider(request):

    try:
        request_data = json.loads(request.body.decode("utf-8"))

        FirebaseID = request_data['user_id']
        Name = request_data['user_name']
        Phone = request_data['user_phn']
        Email = request_data['user_mail']
        Address = request_data['user_address']
        Gender = request_data['user_gender']
        DateOfBirth = request_data['user_dob']
        Photo = request_data['user_photo']

        try:
            Rider.objects.create(FirebaseID=FirebaseID, Name=Name, Phone=Phone, Email=Email, Address=Address,
                                 Gender=Gender, DateOfBirth=DateOfBirth, Photo=Photo)

            data = {
                'msg': 'Success'
            }

        except Exception as e:
            data = {
                'msg': 'Wrong Information or Format',
                'Error': str(e)
            }

        return Response(data)
    except:
        return Response({'msg':'wrong information format'})



@api_view(['POST'])
def delete_driver_details(request, fb_uid):

    try:
        driver = Driver.objects.get(FirebaseID=fb_uid).delete()

        return Response({'msg': fb_uid+' User Deleted'})
    except:
        return Response({'msg':'No User Found'})


@api_view(['POST'])
def delete_rider_details(request, fb_uid):

    try:
        driver = Rider.objects.get(FirebaseID=fb_uid).delete()

        return Response({'msg': fb_uid+' User Deleted'})
    except:
        return Response({'msg':'No User Found'})



@api_view(['POST'])
def car_update(request,id):

    try:

        data = request.data
        car_info = Car.objects.get(FirebaseID = id)

        car_info.Model = data['Model']
        car_info.Color = data['Color']
        car_info.Type = data['Type']
        car_info.RegistrationNumber = data['RegistrationNumber']
        car_info.isAC = data['isAC']
        car_info.Condition = data['Condition']
        car_info.Pictures = data['Pictures']
        car_info.save()

        return Response({
                'Message' : 'Details Update Successfully'
            })

    except:
        return Response({
            'Message' : 'No content found'

            })

@api_view(['POST'])
def driver_update(request,id):
    try:
        # request_data = json.loads(request.body.decode("utf-8"))
        rider = Driver.objects.get(FirebaseID=id)

        serializer = DriverSerializer(rider, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            data = {
                'msg': 'Wrong Information or Format',
            }
            return Response(data)

    except:
        return Response({'msg': 'wrong information format'})

@api_view(['POST'])
def rider_update(request):
    try:
        request_data = json.loads(request.body.decode("utf-8"))
        rider = Rider.objects.get(ID=request_data['ID'])

        serializer = RiderSerializer(rider, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            data = {
                'msg': 'Wrong Information or Format',
            }
            return Response(data)

    except:
        return Response({'msg': 'wrong information format'})

