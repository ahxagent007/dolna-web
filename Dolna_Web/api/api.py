from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_car_details(request, driver_id):
    data = {}
    return Response(data)