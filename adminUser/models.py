from django.contrib.auth.models import AbstractUser
from django.db import models


class UserMaster(models.Model):
    user_tpe = models.CharField(max_length=255,null=True,blank=True)
    status = models.BooleanField(null=False,blank=False)


class CustomUser(AbstractUser):
    adminUser = models.BooleanField(default=False)
    recruiter = models.BooleanField(default=False)
    client = models.BooleanField(default=False)
    associate = models.BooleanField(default=False)
    trainee = models.BooleanField(default=False)
    consultant = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True,blank=True)
    phone = models.CharField(max_length=255,null=True,blank=True)
    employee_id = models.CharField(max_length=255,unique=True,null=True,blank=True)
    rawpassword = models.CharField(max_length=255,null=True, blank=True)





class SalarySlipDetail(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=255,null=True, blank=True)
    employee_name = models.CharField(max_length=255,null=True,blank=True)
    client_name =  models.CharField(max_length=255,null=True,blank=True)
    client_location = models.CharField(max_length=255,null=True,blank=True)
    employee_type = models.CharField(max_length=255,null=True,blank=True)
    basic = models.IntegerField(null=True,blank=True)
    HRA  = models.IntegerField(null=True,blank=True)
    conveyance  = models.IntegerField(null=True,blank=True)
    Other_allowance  = models.IntegerField(null=True,blank=True)
    gross_salary  = models.IntegerField(null=True,blank=True)
    employer_PF  = models.IntegerField(null=True,blank=True)
    employer_ESIC  = models.IntegerField(null=True,blank=True)
    employee_PF  = models.IntegerField(null=True,blank=True)
    employee_ESIC  = models.IntegerField(null=True,blank=True)
    TDS  = models.IntegerField(null=True,blank=True)
    professional_tax  = models.IntegerField(null=True,blank=True)
    CTC  = models.IntegerField(null=True,blank=True)
    in_hand_salary  = models.IntegerField(null=True,blank=True)
    pb_incentive_payable  = models.IntegerField(null=True,blank=True)
    net_payable  = models.IntegerField(null=True,blank=True)
    year = models.CharField(max_length=255,null=True,blank=True)
    month = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)



class ClientRecruiterMapping(models.Model):
    adminuser_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='adminuser_set')
    recruiter_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recruiter_set')
    client_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client_set')
