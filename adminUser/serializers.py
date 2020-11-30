from allauth.account.adapter import get_adapter
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.encoding import force_text
from rest_auth.models import TokenModel
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model, update_session_auth_hash
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlsafe_base64_decode as uid_decoder

from adminUser.models import CustomUser, SalarySlipDetail
from crowning_apis import settings

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'date_joined',
                  'last_login','is_superuser', 'adminUser', 'recruiter', 'client', 'associate', 'trainee', 'consultant','created_by', 'phone', 'employee_id','is_active']


class MyCustomTokenSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = TokenModel
        fields = ('key', 'user')

    class Meta:
        model = TokenModel
        fields = ('key', 'user', 'user_type')

    def get_user_type(self, obj):
        serializer_data = UserSerializer(
            obj.user
        ).data
        adminUser = serializer_data.get('adminUser')
        recruiter = serializer_data.get('recruiter')
        client = serializer_data.get('client')
        associate = serializer_data.get('associate')
        trainee = serializer_data.get('trainee')
        consultant = serializer_data.get('consultant')
        is_superuser = serializer_data.get('is_superuser')

        return {
            'is_superuser': is_superuser,
            'adminUser': adminUser,
            'recruiter': recruiter,
            'client': client,
            'associate': associate,
            'trainee': trainee,
            'consultant': consultant
        }

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField(max_length=255)
    is_superuser = serializers.BooleanField()
    adminUser = serializers.BooleanField()
    recruiter = serializers.BooleanField()
    client = serializers.BooleanField()
    associate = serializers.BooleanField()
    trainee = serializers.BooleanField()
    consultant = serializers.BooleanField()
    created_by = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    employee_id = serializers.CharField(required=False)
    is_active = serializers.BooleanField()



    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'date_joined',
                  'last_login','is_superuser', 'adminUser', 'recruiter', 'client', 'associate', 'trainee', 'consultant', 'password', 'created_by', 'phone', 'employee_id','is_active')


    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone', ''),
            'adminUser': self.validated_data.get('adminUser', ''),
            'recruiter': self.validated_data.get('recruiter', ''),
            'client': self.validated_data.get('client', ''),
            'associate': self.validated_data.get('associate', ''),
            'trainee': self.validated_data.get('trainee', ''),
            'consultant': self.validated_data.get('consultant', ''),
            'created_by': self.validated_data.get('created_by', ''),
            'employee_id': self.validated_data.get('employee_id', ''),
            'is_superuser': self.validated_data.get('is_superuser', ''),
            'is_active': self.validated_data.get('is_active', ''),



        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.phone = self.cleaned_data.get('phone')
        user.adminUser = self.cleaned_data.get('adminUser')
        user.recruiter = self.cleaned_data.get('recruiter')
        user.client = self.cleaned_data.get('client')
        user.associate = self.cleaned_data.get('associate')
        user.trainee = self.cleaned_data.get('trainee')
        user.consultant = self.cleaned_data.get('consultant')
        user.employee_id = self.cleaned_data.get('employee_id')
        user.created_by = self.cleaned_data.get('created_by')
        created_by = self.cleaned_data.get('created_by')
        user.rawpassword = self.cleaned_data.get('password1')
        user.is_superuser = self.cleaned_data.get('is_superuser')
        user.is_active = self.cleaned_data.get('is_active')

        if created_by == '':
            user.created_by = None
        user.save()
        adapter.save_user(request, user, self)
        return user










############  Password Reset #############


class PasswordResetSerializer(serializers.Serializer):

    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(
            data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        if not UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Invalid e-mail address'))

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    phone = serializers.CharField(required=True)
    # token = serializers.CharField(required=True)

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            # phone = force_text(uid_decoder(attrs['phone']))
            self.user = UserModel._default_manager.get(pk=attrs['phone'])
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'phone': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        # if not default_token_generator.check_token(self.user, attrs['token']):
        #     raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:

            update_session_auth_hash(self.request, self.user)





#############################################################################################################################
class GetAllAppUserlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (  "id", "is_superuser","username","first_name",  "last_name","email","is_active","adminUser","recruiter","client","associate","trainee","consultant","created_by","phone","employee_id")

#############################################################################################################################
class SalarySlipDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = SalarySlipDetail
        fields = '__all__'
