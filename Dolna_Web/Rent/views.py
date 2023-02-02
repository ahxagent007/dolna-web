from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from .models import *

# Create your views here.
def StartRent(request):

    request.session['current_page'] = 'Rent'
    context = {

    }
    return render(request, 'rent/start_rent.html', context)


class CarCreate(APIView):

    def post(self,request):
        serializer = CarSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'Message' : 'Car Details added Successfully'
        })

class CarDetails(APIView):

    def get(self,request,id):
        try:
            car_info = Car.objects.get(F_ID = id)

            serializer = CarSerializer(car_info)

            return Response(serializer.data)

        except:
            return Response({
            'Message' : 'No content found'

            })

class CarUpdate(APIView):

    def put(self,request,id):

        try:

            data = request.data
            car_info = Car.objects.get(F_ID = id)

            car_info.Model = data['model']
            car_info.Color = data['color']
            car_info.Type = data['type']
            car_info.RegistrationNumber = data['registrationnumber']
            car_info.isAC = data['isac']
            car_info.Condition = data['condition']
            car_info.Pictures = data['pictures']
            car_info.save()

            return Response({
                'Message' : 'Details Update Successfully'
            })

        except:
            return Response({
            'Message' : 'No content found'

            })