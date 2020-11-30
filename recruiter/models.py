from django.db import models

from adminUser.models import CustomUser


class OfferLetter(models.Model):
    employment_status_choice = (
        ("Employed", "Employed"),
        ("Contract", "Contract"),
        ("Terminated", "Terminated")
    )
    employee_type_choice = (
        ("Associate", "Associate"),
        ("Trainee", "Trainee"),
        ("Consultant", "Consultant")
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    employee_type = models.CharField(max_length=1000, null=True, blank=True, choices=employee_type_choice)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    office_location = models.CharField(max_length=1000, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    reporting_joining_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    approval_on_eonboarding = models.BooleanField(default=False)
    employment_status = models.CharField(max_length=1000, null=True, blank=True, choices=employment_status_choice)
    basic_salary_monthly = models.IntegerField(null=True, blank=True)
    house_rent_allwance_monthly = models.IntegerField(null=True, blank=True)
    other_allwance_monthly = models.IntegerField(null=True, blank=True)
    employee_ESIC_monthly = models.IntegerField(null=True, blank=True)
    employer_ESIC_monthly = models.IntegerField(null=True, blank=True)
    ctc_monthly = models.IntegerField(null=True, blank=True)
    basic_salary_annually = models.IntegerField(null=True, blank=True)
    house_rent_allwance_annually = models.IntegerField(null=True, blank=True)
    other_allwance_annually = models.IntegerField(null=True, blank=True)
    employee_ESIC_annually = models.IntegerField(null=True, blank=True)
    employer_ESIC_annually = models.IntegerField(null=True, blank=True)
    ctc_annually = models.IntegerField(null=True, blank=True)
    HRA = models.IntegerField(null=True,blank=True)
    TDS = models.IntegerField(null=True, blank=True)
    employer_pf_monthly = models.IntegerField(null=True,blank=True)
    employer_pf_annually = models.IntegerField(null=True, blank=True)
    employee_pf_monthly = models.IntegerField(null=True, blank=True)
    employee_pf_annually = models.IntegerField(null=True, blank=True)
    conveyance_monthly = models.IntegerField(null=True, blank=True)
    conveyance_annually = models.IntegerField(null=True, blank=True)
    in_hand_salary = models.IntegerField(null=True, blank=True)
    pb_incentive_payable = models.IntegerField(null=True,blank=True)
    net_payable = models.IntegerField(null=True,blank=True)
    probation_duration = models.IntegerField(null=True,blank=True)
    created_by = models.IntegerField(null=True, blank=True)






class phoneModel(models.Model):
    Mobile = models.CharField(max_length=255,blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)
    def __str__(self):
        return str(self.Mobile)





class Location(models.Model):
    house_no = models.CharField(max_length=200, null=True, blank=True)
    street_blok_name_address = models.CharField(max_length=1000, null=True, blank=True)
    post_office = models.CharField(max_length=255, null=True, blank=True)
    pin_code = models.CharField(max_length=1000, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    poc = models.CharField(max_length=255,null=True,blank=True)
    assigned_poc = models.CharField(max_length=255, null=True, blank=True)


class LocationClientMapping(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)



