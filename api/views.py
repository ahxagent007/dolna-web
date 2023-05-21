from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from functions.common import random_str_generate, random_number
from rest_framework.response import Response
from User.models import DeviceVerification, OTP
import requests
from dotenv import load_dotenv
import os

class OTPToken(APIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsStaff]

    def post(self, request):
        '''
        {
            "serial": "123654987798",
            "device": "asd asd",
            "name": "oneplus"
        }
        '''

        random_str = random_str_generate()

        DeviceVerification.objects.create(serial = request.data['serial'], device = request.data['device'],
                                            name = request.data['name'], token = random_str)

        return Response(data={'token': random_str}, status=status.HTTP_200_OK)

class OTPSend(APIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsStaff]

    def post(self, request):
        '''
        {
            "phone": "01673398900",
            "serial": "asdasdas",
            "token": "asdawdasdasd"
        }
        '''
        load_dotenv()

        phone = request.data['phone']
        serial = request.data['serial']
        token = request.data['token']
        API_KEY = os.getenv("SMS_API_KEY")
        otp = random_number()

        url = "https://api.sms.net.bd/sendsms"

        if len(phone) == 11:

            try:
                device_otp = DeviceVerification.objects.get(serial=serial)
                if device_otp.token == token:
                    payload = {'api_key': API_KEY,
                               'msg': 'Your DOLNA Ride OPT is '+str(otp)+' DO NOT SHARE THIS OTP. Powered by AlphaCue Technologies.',
                               'to': '88'+phone
                               }

                    response = requests.request("POST", url, data=payload).json()
                    if response['error'] == 0:
                        #create OTP data
                        try:
                            otp_mobile = OTP.objects.get(phone = phone)
                            return Response({'error': 'e104_oe'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                        except:
                            OTP.objects.create(phone = phone, otp = otp)
                            device_otp.delete()

                            return Response({'msg': 'OTP sent'}, status=status.HTTP_200_OK)
                    elif response['error'] == 400:
                        #The request was rejected, due to a missing or invalid parameter.
                        return Response({'error': 'e100_400'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    elif response['error'] == 403:
                        #You don't have permissions to perform the request.
                        return Response({'error': 'e100_403'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    elif response['error'] == 404:
                        #The requested resource not found.
                        return Response({'error': 'e100_404'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    elif response['error'] == 405:
                        #Authorization required.
                        return Response({'error': 'e100_405'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    elif response['error'] == 409:
                        #Unknown error occurred on Server end.
                        return Response({'error': 'e100_409'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    elif response['error'] == 410:
                        #Account expired
                        return Response({'error': 'e100_410'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    elif response['error'] == 415:
                        #Message is too long
                        return Response({'error': 'e100_415'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    elif response['error'] == 416:
                        #No valid number found
                        return Response({'error': 'e100_416'}, status=status.HTTP_406_NOT_ACCEPTABLE)

                else:
                    return Response({'error': 'e103_oi'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except Exception as e:
                return Response({'error':'e102_donf'},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'error':'e101_pnc'}, status=status.HTTP_406_NOT_ACCEPTABLE)

class OTPVerify(APIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsStaff]

    def post(self, request):
        '''
        {
            "phone": "01673398900",
            "otp": "123456"
        }
        '''
        phone = request.data['phone']
        otp = request.data['otp']

        try:
            otp_mobile = OTP.objects.get(phone=phone)
            if otp_mobile.otp == otp:
                otp_mobile.delete()
                return Response({'msg':'Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'e106_io'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response({'error': 'e105_onf'}, status=status.HTTP_406_NOT_ACCEPTABLE)