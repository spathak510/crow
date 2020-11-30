from rest_framework import serializers

from adminUser.models import CustomUser
from recruiter.models import OfferLetter, Location


class OfferLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferLetter
        fields = "__all__"




class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ( 'id', 'employee_id', 'first_name', 'last_name', 'email', 'phone','created_by')


class recruiterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ( 'id', 'employee_id', 'first_name', 'last_name', 'email', 'phone','created_by')



class ClientLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"




