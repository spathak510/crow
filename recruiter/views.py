import smtplib
from rest_framework import generics
from rest_framework.permissions import AllowAny
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from .models import phoneModel, Location, LocationClientMapping
import base64
from adminUser.models import CustomUser
from crowning_apis import settings
from recruiter.models import OfferLetter
from recruiter.serializers import OfferLetterSerializer, ClientListSerializer, ClientLocationSerializer, \
    recruiterListSerializer


################################## SEND EMAIL #########################################################################
def send_email(Mail_Subject, Body, toaddr):
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = ", ".join(toaddr)
    msg['Subject'] = Mail_Subject
    body = Body
    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    text = msg.as_string()
    s.sendmail(settings.EMAIL_HOST_USER, toaddr, text)
    s.quit()

#########################################   SEND SMS   ##################################################################

# !/usr/bin/env python

import urllib.request
import urllib.parse


def sendSMS(apikey, numbers, sender, message):
    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                   'message': message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return (fr)



###################################  Sent login credential on Email ##################################################################

class AppuserOfferletterCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = OfferLetter.objects.all()
    serializer_class = OfferLetterSerializer
    # def perform_create(self, serializer):
    #     serializer.save()
    def perform_create(self, serializer):
        serializer.save()
        user_id = serializer.data['user']
        user_obj = CustomUser.objects.get(id=user_id)
        user_email = user_obj.email
        user_first_name = user_obj.first_name
        Mail_Subject = 'Your login credential'
        Mail_body = ("WELCOME TO THE TEAM!\n" +''+ "\n" +
       "Glad for you to be joining us.\n" +''+ "\n" +
       "Here are your login credentials.\n"+
                     ''+"\n"+''+"Email: "+user_email+"\n"+
                     ''+"Password: "+user_obj.rawpassword)
        try:
            send_email(Mail_Subject, Mail_body, user_email)
        except Exception as e:
            pass

##################################### OTP creation And Verification  ################################################################
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class getPhoneNumberRegistered(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            phoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = phoneModel.objects.get(Mobile=phone)
        Mobile.counter += 1
        Mobile.save()
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())
        OTP = pyotp.HOTP(key)

        resp = sendSMS('BvcO5uoam1c-xU3uC7vHtxrn73qicsxoMdUZuIOHhi', Mobile,'9630088330', 'This is your OTP')
        return Response({"OTP": OTP.at(Mobile.counter)}, status=200)


    @staticmethod
    def post(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())
        OTP = pyotp.HOTP(key)
        try:
            if OTP.verify(request.data["OTP"], Mobile.counter):
                Mobile.isVerified = True
                Mobile.save()
                return Response("You are authorised", status=200)
        except Exception as e:
            pass
        return Response("OTP is wrong", status=400)


############################# Get Client list By AdminUser Id    #########################################################

class ClientListByAdminuserId(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = CustomUser.objects.filter(created_by=kwargs['pk'],client=True)
        serializer = ClientListSerializer(object, many=True)
        return Response(serializer.data)




############################# Get Recruiter list By AdminUser Id    #########################################################

class RecruiterListByAdminuserId(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = CustomUser.objects.filter(created_by=kwargs['pk'],recruiter=True)
        serializer = recruiterListSerializer(object, many=True)
        return Response(serializer.data)



############################# Client location mapping    #########################################################


class ClientLocationMappingCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Location.objects.all()
    serializer_class = ClientLocationSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user')
        location = request.data.get('location')
        user_obj = CustomUser.objects.get(id=user)
        status = '201 Created'

        try:
            for item in location:
                house_no = item.get('house_no')
                street_blok_name_address = item.get('street_blok_name_address')
                post_office = item.get('post_office')
                pin_code = item.get('pin_code')
                district = item.get('district')
                state = item.get('state')
                country = item.get('country')
                poc = item.get('poc')
                assigned_poc = item.get('assigned_poc')

                location_obj_creation = Location.objects.create(house_no=house_no,
                                                            street_blok_name_address=street_blok_name_address,
                                                            post_office=post_office, pin_code=pin_code, district=district,
                                                                state=state,country=country,poc=poc,assigned_poc=assigned_poc)

                location_client_mapping_obj = LocationClientMapping.objects.create(user=user_obj,location=location_obj_creation)
        except Exception as e:
            if e:
                status = str(e)


        return Response(json.dumps(status))


############################# Get Client location list By client Id    #########################################################

class ClientLocationList(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        data = []
        object = LocationClientMapping.objects.filter(user_id=kwargs['pk'])
        for item in object:
            data.append({'location_id':item.location_id,'poc':item.location.poc,'assigned_poc':item.location.assigned_poc,'house_no':item.location.house_no,
                         'street_blok_name_address':item.location.street_blok_name_address,
                         'post_office':item.location.post_office, 'pin_code':item.location.pin_code,
                         'district':item.location.district,'state':item.location.state,'country':item.location.country})

        return Response(data)





################################### delete client location ################################################################
class ClientLocationDeleteView(APIView):
    permission_classes = (AllowAny,)

    def delete(self, request, pk, format=None):
        status = '200'
        result='Location id'+''+str(pk)+''+'deleted successfully.'
        try:
            LocationClientMapping_obj = LocationClientMapping.objects.get(location_id=pk)
            snippet = Location.objects.get(id=pk)
            LocationClientMapping_obj.delete()
            snippet.delete()
        except Exception as e:
            if e:
                result=e
        return Response({"status":status, "result":result})

################################### Update client location ################################################################
class ClientLocationUpdateView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, format=None):
        data = request.data
        location_id = data.get('location_id')
        poc = data.get('poc')
        assigned_poc = data.get('assigned_poc')
        status = '200'
        result='Location id'+'deleted successfully.'
        try:
            location_obj = Location.objects.get(id=location_id)
            location_obj.poc = poc
            location_obj.assigned_poc = assigned_poc
            location_obj.save();
        except Exception as e:
            if e:
                status=e
        return Response({"status":status, "result":result})