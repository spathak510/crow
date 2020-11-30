import boto3
import os
from threading import Timer
from kombu.utils import json
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from adminUser.models import CustomUser
from adminUser.views import save_file, remove_file
from appUser.models import PersonalDetails, EducationDetails, FamilyDetails, WorkExperience, \
    KYC, EPF, ESIC, Media, ChildrenDetails, ChildrenAppuserMapping, AadharVerification
from appUser.serializers import PersonalDetailSerializer, EducationDetailSerializer, FamilyDetailSerializer, \
    WorkExperienceSerializer, KYCSerializer, EPFSerializer, ESICSerializer, AppuserListSerializer, \
    AppuserDocumentListSerializer, AadharSerializer
from crowning_apis import settings


class AppuserPersonaldetailsCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = PersonalDetails.objects.all()
    serializer_class = PersonalDetailSerializer


    def perform_create(self, serializer):
        serializer.save()


############################# Get AppUser personal details By Appuser Id    #########################################################

class AppuserPersonaldetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = PersonalDetails.objects.filter(user_id=kwargs['pk'])
        serializer = PersonalDetailSerializer(object, many=True)
        return Response(serializer.data)



# class AppuserEducationDetailCreateView(generics.ListCreateAPIView):
#     permission_classes = (AllowAny,)
#     queryset = EducationDetails.objects.all()
#     serializer_class = EducationDetailSerializer
#
#     def create(self, request, *args, **kwargs):
#         user = request.data.get('user')
#         education = request.data.get('education')
#         user_obj = CustomUser.objects.get(id=user)
#         status = '201 Created'
#         s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_AccessKeyId,
#                                  aws_secret_access_key=settings.AWS_SecretKey)
#         bucket = 'crowning'
#         try:
#             for item in education:
#                 degree_qualification = item.get('degree_qualification')
#                 institute_name = item.get('institute_name')
#                 board_university = item.get('board_university')
#                 percentage_GPA = item.get('percentage_GPA')
#                 passout_year = item.get('passout_year')
#                 key = item.get('exit_letter')
#                 EducationDetails_obj_creation = EducationDetails.objects.create(user=user_obj, degree_qualification=degree_qualification,
#                                                             institute_name=institute_name,
#                                                             board_university=board_university,
#                                                              percentage_GPA=percentage_GPA, passout_year=passout_year)
#
#                 s3_client.upload_file(key, bucket, 'root/educationDocument/' + key)
#                 obj = Media.objects.create(user=user_obj, document_type='education_document',
#                                            file_url='https://crowning.s3.amazonaws.com/root/educationDocument/' + key)
#         except Exception as e:
#             if e:
#                 status = str(e)
#         return Response(json.dumps(status))


class AppuserEducationDetailCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = EducationDetails.objects.all()
    serializer_class = EducationDetailSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        status = '201 Created'
        try:
            s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_AccessKeyId,aws_secret_access_key=settings.AWS_SecretKey)
            bucket = 'crowning'
            user = data.get('user')
            user_obj = CustomUser.objects.get(id=user)
            degree_qualification = data.get('degree_qualification')
            institute_name = data.get('institute_name')
            board_university = data.get('board_university')
            percentage_GPA = data.get('percentage_GPA')
            passout_year = data.get('passout_year')

            EducationDetails_obj_creation = EducationDetails.objects.create(user=user_obj, degree_qualification=degree_qualification,
                                                        institute_name=institute_name,
                                                        board_university=board_university,
                                                         percentage_GPA=percentage_GPA, passout_year=passout_year)
            for f in request.FILES.getlist('files'):
                key = save_file(f)
                file_path = degree_qualification + '_' + key
                s3_client.upload_file(key, bucket, 'root/educationDocument/' + degree_qualification + '_' + key)
                obj = Media.objects.create(user=user_obj, document_type='education_document',file_url='https://crowning.s3.amazonaws.com/root/educationDocument/' + file_path)

                os.remove(key)
        except Exception as e:
            if e:
                status = e
        return Response(json.dumps(status))


############################# Get AppUser personal details By Appuser Id    #########################################################

class AppuserEducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = EducationDetails.objects.filter(user_id=kwargs['pk'])
        serializer = EducationDetailSerializer(object, many=True)
        return Response(serializer.data)






class AppuserFamilyDetailCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = FamilyDetails.objects.all()
    serializer_class = FamilyDetailSerializer

    def create(self, request, *args, **kwargs):
        status = '201 Created'
        data = request.data
        user_id = data.get('user')
        user_obj = CustomUser.objects.get(id=user_id)
        father_name = data.get('father_name')
        father_DOB = data.get('father_DOB')
        father_residing_with_you = data.get('father_residing_with_you')
        mother_name = data.get('mother_name')
        mother_DOB = data.get('mother_DOB')
        mother_residing_with_you = data.get('mother_residing_with_you')
        father_place_of_residence = data.get('father_place_of_residence')
        father_insurance_persentage = data.get('father_insurance_persentage')
        mother_place_of_residence = data.get('mother_place_of_residence')
        mother_insurance_persentage = data.get('mother_insurance_persentage')
        spouse_place_of_residence = data.get('spouse_place_of_residence')
        spouse_insurance_persentage = data.get('spouse_insurance_persentage')
        spouse_residing_with_you = data.get('spouse_residing_with_you')
        spouse_name = data.get('spouse_name')
        spouse_DOB = data.get('spouse_DOB')
        spouse_gender = data.get('spouse_gender')
        children = data.get('children')
        obj = FamilyDetails.objects.create(user=user_obj,father_name=father_name,father_DOB=father_DOB,father_residing_with_you=father_residing_with_you,mother_name=mother_name,mother_DOB=mother_DOB,
                                           mother_residing_with_you=mother_residing_with_you,
                                           father_place_of_residence=father_place_of_residence,
                                           father_insurance_persentage=father_insurance_persentage,
                                           mother_place_of_residence=mother_place_of_residence,
                                           mother_insurance_persentage=mother_insurance_persentage,
                                           spouse_name=spouse_name,spouse_DOB=spouse_DOB,
                                           spouse_gender=spouse_gender,spouse_residing_with_you=spouse_residing_with_you,
                                           spouse_place_of_residence=spouse_place_of_residence,spouse_insurance_persentage=spouse_insurance_persentage,
                                           children=children)

        children_detail = data.get('children_detail')


        try:
            for item in children_detail:
                children_name = item.get('children_name')
                children_gender = item.get('children_gender')
                children_place_of_residence = item.get('children_place_of_residence')
                children_insurance_persentage = item.get('children_insurance_persentage')
                ChildrenDetails_obj_creation = ChildrenDetails.objects.create(children_name=children_name, children_gender=children_gender,
                                                            children_place_of_residence=children_place_of_residence,
                                                            children_insurance_persentage=children_insurance_persentage)

                ChildrenAppuserMapping_obj_creation = ChildrenAppuserMapping.objects.create(user=user_obj,children_id=ChildrenDetails_obj_creation)
        except Exception as e:
            if e:
                status = str(e)


        return Response(json.dumps(status))





############################# Get appuser Family details by appuser ID #######################################################

class AppuserFamilyDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = FamilyDetails.objects.get(user_id=kwargs['pk'])
        serializer = FamilyDetailSerializer(object)
        return Response(serializer.data)

############################# Get Client location list By client Id    #########################################################

class AppuserChildrenList(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        data = []
        object = ChildrenAppuserMapping.objects.filter(user_id=kwargs['pk'])
        for item in object:
            data.append({'children_id':item.children_id_id,'children_name':item.children_id.children_name,'children_gender':item.children_id.children_gender,
                         'children_place_of_residence':item.children_id.children_place_of_residence,
                         'children_insurance_persentage':item.children_id.children_insurance_persentage})

        return Response(data)




##################################### After Aadhar Verification  ########################################################
class AadharVerificationCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = AadharVerification.objects.all()
    serializer_class = AadharSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        status = '201 Created'
        try:
            s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_AccessKeyId, aws_secret_access_key=settings.AWS_SecretKey)
            bucket = 'crowning'
            user = data.get('user')
            user_obj = CustomUser.objects.get(id=user)
            aadhar_number = data.get('aadhar_number')
            isVerified = data.get('isVerified')

            AadharVerification_obj_creation = AadharVerification.objects.create(user=user_obj, aadhar_number=aadhar_number,isVerified=isVerified)
            for f in request.FILES.getlist('files'):
                key = save_file(f)
                file_path = aadhar_number + '_' + key
                s3_client.upload_file(key, bucket, 'root/aadhar_document/' + aadhar_number + '_' + key)
                obj = Media.objects.create(user=user_obj, document_type='aadhar_document',file_url='https://crowning.s3.amazonaws.com/root/aadhar_document/' + file_path)

                os.remove(key)
        except Exception as e:
            if e:
                status = e
        return Response(json.dumps(status))


class AppuserWorkExperienceCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer

    def create(self, request, *args, **kwargs):
        status = '201 Created'
        data = request.data
        try:
            user = data.get('user')
            user_obj = CustomUser.objects.get(id=user)
            s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_AccessKeyId,aws_secret_access_key=settings.AWS_SecretKey)
            bucket = 'crowning'
            work_experience_year = data.get('work_experience_year')
            work_experience_month = data.get('work_experience_month')
            currently_employment = data.get('currently_employment')
            company_name = data.get('company_name')
            position = data.get('position')
            joining_date = data.get('joining_date')
            ctc = data.get('ctc')
            company_address = data.get('company_address')
            employee_code = data.get('employee_code')
            reporting_manager = data.get('reporting_manager')
            relationship_with_reporting_manager = data.get('relationship_with_reporting_manager')
            previous_work_experience = data.get('previous_work_experience')
            WorkExperience_obj_creation = WorkExperience.objects.create(user=user_obj, work_experience_year=work_experience_year,
                                                        work_experience_month=work_experience_month,
                                                        currently_employment=currently_employment
                                                        , company_name=company_name, position=position,
                                                        joining_date=joining_date,
                                                        ctc=ctc, company_address=company_address,
                                                        employee_code=employee_code,
                                                        reporting_manager=reporting_manager,
                                                        relationship_with_reporting_manager=relationship_with_reporting_manager,
                                                        previous_Work_experience=previous_work_experience)
            for f in request.FILES.getlist('files'):
                key = save_file(f)
                file_path = company_name + '_' + key
                s3_client.upload_file(key, bucket, 'root/workExperience/' + company_name + '_' + key)
                obj = Media.objects.create(user=user_obj, document_type='workExperience_document',file_url='https://crowning.s3.amazonaws.com/root/workExperience/' + file_path)

                os.remove(key)
        except Exception as e:
            if e:
                status = e

        return Response(json.dumps(status))


############################# Get AppUser work experience details By Appuser Id    #########################################################

class AppuserWorkExperienceView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = WorkExperience.objects.filter(user_id=kwargs['pk'])
        serializer = WorkExperienceSerializer(object, many=True)
        return Response(serializer.data)






# class AppuserKYCCreateView(generics.ListCreateAPIView):
#     permission_classes = (AllowAny,)
#     queryset = KYC.objects.all()
#     serializer_class = KYCSerializer
#
#
#     def perform_create(self, serializer):
#         serializer.save()


class AppuserKYCCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = KYC.objects.all()
    serializer_class = KYCSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        status = '201 Created'
        try:
            s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_AccessKeyId,aws_secret_access_key=settings.AWS_SecretKey)
            bucket = 'crowning'
            user = data.get('user')
            user_obj = CustomUser.objects.get(id=user)
            have_pan_number = data.get('have_pan_number')
            pan_number = data.get('pan_number')
            bank_account_number = data.get('bank_account_number')
            re_bank_account_number = data.get('re_bank_account_number')
            bank_name = data.get('bank_name')
            branch_name = data.get('branch_name')
            IFSC_code = data.get('IFSC_code')
            internation_worker = data.get('internation_worker')
            country_of_origin = data.get('country_of_origin')
            passport_number = data.get('passport_number')
            passport_validity_from = data.get('passport_validity_from')
            passport_validity_to = data.get('passport_validity_to')

            pan_card_file = request.FILES.getlist('pan_card_file')
            bank_document_file = request.FILES.getlist('bank_document_file')
            passport_file = request.FILES.getlist('passport_file')

            KYC_obj_creation = KYC.objects.create(user=user_obj, have_pan_number=have_pan_number,pan_number=pan_number,
                                                        bank_account_number=bank_account_number,re_bank_account_number=re_bank_account_number,
                                                        bank_name=bank_name,branch_name=branch_name,IFSC_code=IFSC_code,internation_worker=internation_worker,
                                                         country_of_origin=country_of_origin, passport_number=passport_number,passport_validity_from=passport_validity_from,
                                                  passport_validity_to=passport_validity_to)
            if pan_card_file:
                for f in request.FILES.getlist('pan_card_file'):
                    key = save_file(f)
                    file_path = 'pan_card_file' + '_' + key
                    s3_client.upload_file(key, bucket, 'root/userKYC/' + 'pan_card_file' + '_' + key)
                    obj = Media.objects.create(user=user_obj, document_type='user_KYC',file_url='https://crowning.s3.amazonaws.com/root/userKYC/' + file_path)
                    os.remove(key)

            if bank_document_file:
                for f in request.FILES.getlist('bank_document_file'):
                    key = save_file(f)
                    file_path = 'bank_document_file' + '_' + key
                    s3_client.upload_file(key, bucket, 'root/userKYC/' + 'bank_document_file' + '_' + key)
                    obj = Media.objects.create(user=user_obj, document_type='user_KYC',file_url='https://crowning.s3.amazonaws.com/root/userKYC/' + file_path)
                    os.remove(key)

            if passport_file:
                for f in request.FILES.getlist('passport_file'):
                    key = save_file(f)
                    file_path = 'passport_file' + '_' + key
                    s3_client.upload_file(key, bucket, 'root/userKYC/' + 'passport_file' + '_' + key)
                    obj = Media.objects.create(user=user_obj, document_type='user_KYC',file_url='https://crowning.s3.amazonaws.com/root/userKYC/' + file_path)
                    os.remove(key)
        except Exception as e:
            if e:
                status = e
        return Response(json.dumps(status))


############################# Get AppUser KYC details By Appuser Id    #########################################################

class AppuserKYCDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = KYC.objects.filter(user_id=kwargs['pk'])
        serializer = KYCSerializer(object, many=True)
        return Response(serializer.data)



class AppuserEPFCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = EPF.objects.all()
    serializer_class = EPFSerializer


    def perform_create(self, serializer):
        serializer.save()


############################# Get AppUser EPFC details By Appuser Id    #########################################################

class AppuserEPFDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = EPF.objects.filter(user_id=kwargs['pk'])
        serializer = EPFSerializer(object, many=True)
        return Response(serializer.data)


class AppuserESICCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = ESIC.objects.all()
    serializer_class = ESICSerializer


    def perform_create(self, serializer):
        serializer.save()

    ############################# Get AppUser EPFC details By Appuser Id    #########################################################

class AppuserESICDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = ESIC.objects.filter(user_id=kwargs['pk'])
        serializer = ESICSerializer(object, many=True)
        return Response(serializer.data)



############################# Get AppUser list By Recruiter Id    #########################################################

class AppuserListByRecruiterId(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = CustomUser.objects.filter(created_by=kwargs['pk'])
        serializer = AppuserListSerializer(object, many=True)
        return Response(serializer.data)



###################################################################################################
class GetUserDocuments(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        data = []
        object = Media.objects.filter(user=kwargs['pk'])
        serializer = AppuserDocumentListSerializer(object, many=True)
        return Response(serializer.data)



# def GetUserDocuments(self, request):
#     data = request.data
    #  s3_resource = boto3.resource('s3',aws_access_key_id=settings.AWS_AccessKeyId,aws_secret_access_key=settings.AWS_SecretKey)
    # my_bucket = s3_resource.Bucket('crowning')
    # objects = my_bucket.objects.filter(Prefix='root/userKYC/bank_document_file_/tmp/')
    # for obj in objects:
    #     path, filename = os.path.split(obj.key)
    #     my_bucket.download_file(obj.key, filename)
#     return Response(data={"files": "{} files uploaded".format(len(key)),
#                           "data": "{} data included".format(len(data))})

