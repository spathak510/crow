from rest_framework import serializers

from adminUser.models import CustomUser
from appUser.models import PersonalDetails, EducationDetails, FamilyDetails, WorkExperience, KYC, EPF, ESIC, Media, \
    AadharVerification


class PersonalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = "__all__"



class EducationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationDetails
        fields = "__all__"



class FamilyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyDetails
        fields = "__all__"





class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = "__all__"


class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = "__all__"


class EPFSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPF
        fields = "__all__"


class ESICSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESIC
        fields = "__all__"





class AppuserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = "__all__"
        fields = ('id','employee_id','first_name','last_name','email','associate','trainee','consultant','phone','created_by')


class AppuserDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"
        # fields = ('id','employee_id','first_name','last_name','email','associate','trainee','consultant','phone','created_by')


class AadharSerializer(serializers.ModelSerializer):
    class Meta:
        model = AadharVerification
        fields = "__all__"
