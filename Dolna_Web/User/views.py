from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from .models import *
# Create your views here.

class DriverRegistration(APIView):

    def post(self,request):
        serializer = DriverSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def get(self,request):
        try:

            driver_info = Driver.objects.get(ID=request.data['id'])

            serializer = DriverSerializer(driver_info)

            return Response(serializer.data)

        except:
            return Response({
            'Message' : 'No content found'

            })

    def put(self,request):

        try:

            data = request.data

            driver_info = Driver.objects.get(ID = request.data['id'])

            driver_info.ID = data['id']
            driver_info.Name = data['name']
            driver_info.Phone = data['phone']
            driver_info.Email = data['email']
            driver_info.Address = data['address']
            driver_info.NID = data['nid']
            driver_info.Photo = data['photo']
            driver_info.save()

            return Response({
                'Message' : 'Details Update Successfully'
            })

        except:
            return Response({
            'Message' : 'No content found'

            })

