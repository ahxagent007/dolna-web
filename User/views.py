# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .serializer import *
# from .models import *
# # Create your views here.
#
# class DriverRegistration(APIView):
#
#     def post(self,request):
#         serializer = DriverSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data)
#
# class DriverDetails(APIView):
#
#     def get(self,request,id):
#         try:
#
#             driver_info = Driver.objects.get(F_ID=id)
#
#             serializer = DriverSerializer(driver_info)
#
#             return Response(serializer.data)
#
#         except:
#             return Response({
#             'Message' : 'No content found'
#
#             })
#
# class DriverUpdate(APIView):
#
#     def put(self,request,id):
#
#         try:
#
#             data = request.data
#
#             driver_info = Driver.objects.get(F_ID = id)
#
#             driver_info.Name = data['name']
#             driver_info.Phone = data['phone']
#             driver_info.Email = data['email']
#             driver_info.Address = data['address']
#             driver_info.NID = data['nid']
#             driver_info.Photo = data['photo']
#             driver_info.save()
#
#             return Response({
#                 'Message' : 'Details Update Successfully'
#             })
#
#         except:
#             return Response({
#             'Message' : 'No content found'
#
#             })
#
