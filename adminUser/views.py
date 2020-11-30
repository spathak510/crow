from threading import Timer
import os
import datetime
import boto3
import pdfkit
import xlrd
from django.shortcuts import render
from rest_framework import status, views
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from appUser.models import Media
from crowning_apis import settings
from recruiter.models import OfferLetter
from django_filters.rest_framework import DjangoFilterBackend
from adminUser.models import CustomUser, SalarySlipDetail, ClientRecruiterMapping
from adminUser.serializers import PasswordResetSerializer, PasswordResetConfirmSerializer, PasswordChangeSerializer, \
    GetAllAppUserlistSerializer, SalarySlipDetailSerializers
from recruiter.views import send_email



########################### Save uploaded files ##########################

def save_file(f):
    file_name = '/tmp/'+ str(f.name)
    try:
        with open(file_name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        destination.close()
    except Exception as e:
        if e:
            file_name = e
    return file_name

################################## Remove created PDF file #######################################
def remove_file(f):
    os.remove(f)
    # for file in os.listdir('/tmp/'):
    #     if file.endswith('.pdf'):
    #         os.remove(f)




############ Reset Password ##################
class PasswordResetView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"success": "Password reset e-mail has been sent."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Password has been reset with the new password."})


class PasswordChangeView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "New password has been saved."})



################################### Upload offerletter in s3 bucket  ################################################

def offerletterView(request):
    id = request.GET.get('userid')
    obj = OfferLetter.objects.get(user_id=id)
    context = {
        'Offer_Letter_Issue_Date': datetime.date.today(),
        'Candidate_name':obj.user.employee_id,
        'Candidate_designation':obj.designation,
        'Client_name':obj.client_name,
        'Client_location':obj.office_location,
        'Candidate_Joining_Date':obj.reporting_joining_date,
        'Cost_to_Company':obj.ctc_annually,
        'Salary_offered':obj.net_payable,
        'probation_duration':obj.probation_duration,
        'Basic_salary_monthly':obj.basic_salary_monthly,
        'Basic_salary_annually':obj.basic_salary_annually,
        'house_rent_allowance_monthly':obj.house_rent_allwance_monthly,
        'house_rent_allowance_annually': obj.house_rent_allwance_annually,
        'transport_monthly': obj.conveyance_monthly,
        'transport_annually':obj.conveyance_annually,
        'other_allowance_monthly': obj.other_allwance_monthly,
        'other_allowance_annually':obj.other_allwance_annually,
        'pf_employer_monthly':obj.employer_pf_annually,
        'pf_employer_annualy':obj.employee_pf_annually,
        'ESIC_monthly': obj.employer_ESIC_monthly,
        'ESIC_annually':obj.employee_ESIC_annually,
        'Tottal_ctc_monthly':obj.ctc_monthly,
        'Tottal_ctc_annually': obj.ctc_annually
    }

    return render(request, "crowning_offerletter.html",context)



def get_pdf(request):
    id = request.GET.get('userid')
    obj = OfferLetter.objects.get(user_id=int(id))
    s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_AccessKeyId,aws_secret_access_key=settings.AWS_SecretKey)
    user_name = obj.user.employee_id
    key = '/tmp/'+user_name+'.pdf'
    bucket = 'crowning'
    try:
        pdf = pdfkit.from_url('http://127.0.0.1:8000/offerletter/view?userid='+str(id), key)
        s3_client.upload_file(key, bucket, 'root/offerletters/'+key)
        media_obj = Media.objects.create(user=obj.user, document_type='offerletter',file_url='https://crowning.s3.amazonaws.com/root/offerletters/' + key)
    except Exception as e:
        pass
    try:
        t = Timer(3 * 60, remove_file(key))
        t.start()
    except Exception as e:
        pass

    user_email = obj.user.email
    user_first_name = obj.user.first_name
    Mail_Subject = 'Offer Letter'
    Mail_body = ('Dear'+' '+ user_first_name+' '+'Congratulations!!\n' + '' + "\n" +
                 "Download your offer letter by click on this link!\n" + '' + "\n" +
                 '' + "Linck: " +media_obj.file_url )
    try:
        send_email(Mail_Subject, Mail_body, user_email)
    except Exception as e:
        pass
    return Response({"status":'200', "result":'Offer Letter sent successfully or your Email.'})









############################# Get All AppUser list  #########################################################

class GetAllAppUserlist(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(adminUser=False,recruiter=False,client=False,is_superuser=False)
    serializer_class = GetAllAppUserlistSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GetAllAppUserlistSerializer(queryset, many=True)
        return Response(serializer.data)

############################# Get All Recruiter list   #########################################################

class GetAllRecruiterlist(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(recruiter=True)
    serializer_class = GetAllAppUserlistSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GetAllAppUserlistSerializer(queryset, many=True)
        return Response(serializer.data)


############################# Get All Client list   #########################################################

class GetAllClientlist(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(client=True)
    serializer_class = GetAllAppUserlistSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GetAllAppUserlistSerializer(queryset, many=True)
        return Response(serializer.data)

############################# Get All adminuser list   #########################################################

class GetAllAdminusertlist(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(adminUser=True)
    serializer_class = GetAllAppUserlistSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GetAllAppUserlistSerializer(queryset, many=True)
        return Response(serializer.data)




######################################### Salary slip creation View ##########################################################
class salarySlipCreation(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        year = request.data.get('year')
        month = request.data.get('month')
        file_obj = request.FILES['salary_slip']
        file = save_file(file_obj)
        wb = xlrd.open_workbook('/tmp/salary_file.xlsx')
        sheet = wb.sheet_by_index(0)
        rows = sheet.nrows
        currept_data = []

        for i in range(1,rows):
            row_data = sheet.row_values(i)
            employee_id       = row_data[0]
            employee_name     = row_data[1]
            client_name       = row_data[2]
            client_location   = row_data[3]
            employee_type     = row_data[4]
            basice            = int(row_data[5])
            hra               = row_data[6]
            conveyance        = int(row_data[7])
            Other_allowance   = int(row_data[8])
            gross_salary      = int(row_data[9])
            employer_PF       = int(row_data[10])
            employer_ESIC     = int(row_data[11])
            employee_PF       = int(row_data[12])
            employee_ESIC     = int(row_data[13])
            TDS               = int(row_data[14])
            professional_tax  = int(row_data[15])
            CTC               = int(row_data[16])
            in_hand_salary    = int(row_data[17])
            pb_incentive_payable = int(row_data[18])
            net_payable = int(row_data[19])

            try:
                user_obj = CustomUser.objects.get(employee_id=employee_id)
                salary_slip_obj = SalarySlipDetail.objects.create(user_id=user_obj,employee_id=employee_id,employee_name=employee_name,client_name=client_name,client_location=client_location,
                                                                  employee_type=employee_type,basic=basice,HRA=hra,conveyance=conveyance,Other_allowance=Other_allowance,gross_salary=gross_salary,
                                                                  employer_PF=employer_PF,employer_ESIC=employer_ESIC,employee_PF=employee_PF,employee_ESIC=employee_ESIC,TDS=TDS,
                                                                  professional_tax=professional_tax,CTC=CTC,in_hand_salary=in_hand_salary,pb_incentive_payable=pb_incentive_payable,
                                                                  net_payable=net_payable,year=year,month=month)
            except Exception as e:
                currept_data.append(employee_id)
                continue


        #key = file
        # s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_AccessKeyId,aws_secret_access_key=settings.AWS_SecretKey)
        # bucket = 'crowning'
        # s3_client.upload_file(key, bucket, 'root/salarySlip/' + key)
        #
        # media_obj = Media.objects.create(user=user_obj, document_type='offerletter',file_url='https://crowning.s3.amazonaws.com/root/salarySlip/' + key)

        os.remove(file)
        user_email= 'xyz321@mailinator.com'
        Mail_Subject = 'Wrong data in salary file.'
        Mail_body = ("Some employee id is not correct! Please check it and upload again salary data corresponding to these employees ids .\n" + '' + "\n" +
                     '' + "Employee ID's: " + str(currept_data))
        try:
            send_email(Mail_Subject, Mail_body, user_email)
        except Exception as e:
            pass
        return Response(status=201)



############################# Get salary details of Appuser   #########################################################
class GetSalarySlipView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = SalarySlipDetail.objects.all()
    serializer_class = SalarySlipDetailSerializers
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user_id', 'year','month']


############################# Delete salary of an employee ##################################################
class DeleteAppuserSalarySlipDataView(APIView):
    permission_classes = (AllowAny,)

    def delete(self, request, format=None):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        employee_id = request.query_params.get('employee_id')
        result= employee_id+' '+ 'salary slip' +' '+month+' '+year+' '+'deleted successfully.'
        satatus = '200'
        try:
            SalarySlipDetail_obj = SalarySlipDetail.objects.get(employee_id=employee_id,year=year,month=month)
            SalarySlipDetail_obj.delete()
        except Exception as e:
            if e:
                result= 'bad request'
                satatus = '400'
        return Response({'status':satatus,'result':result})



####################################### Client Recruiter Mapping and Update and Get######################################
class ClientRecruiterMappingByAdmin(APIView):
    permission_classes = (AllowAny,)

    def post(self,request,formate=None):
        data = request.data
        adminuser_id = data.get('admin_id')
        recruiter_id = data.get('recruiter_id')
        client_id = data.get('client_id')
        admin_obj = CustomUser.objects.get(id=adminuser_id)
        recruiter_obj = CustomUser.objects.get(id=recruiter_id)
        status = '201'
        result = 'client recruiter mapping successfully!'
        try:
            for client in client_id:
                client_obj = CustomUser.objects.get(id=client)
                obj = ClientRecruiterMapping.objects.create(adminuser_id=admin_obj,recruiter_id=recruiter_obj,client_id=client_obj)
        except Exception as e:
            print(e)
        return Response({'satatus':status, 'result':result})



class GetClientRecruiterMappingData(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        data = {}
        s = []
        recruiter_id = request.query_params.get('recruiter_id')
        obj = ClientRecruiterMapping.objects.filter(recruiter_id=recruiter_id)
        for item in obj:
            data.update({"admin_id":item.adminuser_id_id,"admin_name":(item.adminuser_id.first_name+' '+item.adminuser_id.first_name)},)
            data.update({"recruiter_id":item.recruiter_id_id,"recruiter_name":(item.recruiter_id.first_name+' '+item.recruiter_id.first_name)},)
            s.append({"mapping_id":item.id,"client_id":item.client_id_id,"client_name":(item.client_id.first_name+' '+item.client_id.first_name) ,})

        data.update({"mapped_client":s})

        return Response(data)



class ClientRecruiterUnMapping(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, formate=None):
        data = request.data
        mapping_id = data.get('mapping_id')
        status = '200'
        result = 'client recruiter unmapped successfully!'
        try:
            for id in mapping_id:
                obj = ClientRecruiterMapping.objects.get(id=id)
                obj.delete()
        except Exception as e:
            print(e)
        return Response({'satatus': status, 'result': result})



################################### Update client  ################################################################
class ClientUpdateView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, format=None):
        data = request.data
        client_id = data.get('client_id')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        status = '200'
        result='Client id'+' '+str(client_id) +' '+ 'update successfully.'
        try:
            obj = CustomUser.objects.get(id=client_id)
            obj.first_name = first_name
            obj.last_name = last_name
            obj.email = email
            obj.phone = phone
            obj.save();
        except Exception as e:
            if e:
                status=e
        return Response({"status":status, "result":result})


################################### Update Recruiter  ################################################################
class RecruiterUpdateView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, format=None):
        data = request.data
        recruiter_id = data.get('recruiter_id')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        status = '200'
        result = 'Recruiter id'+' '+str(recruiter_id) +' '+ 'update successfully.'
        try:
            obj = CustomUser.objects.get(id=recruiter_id)
            obj.first_name = first_name
            obj.last_name = last_name
            obj.email = email
            obj.phone = phone
            obj.save();
        except Exception as e:
            if e:
                status=e
        return Response({"status":status, "result":result})



