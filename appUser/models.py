from django.db import models
from adminUser.models import CustomUser


class PersonalDetails(models.Model):
    employment_type_choice = (
        ("Associate", "Associate"),
        ("Trainee", "Trainee"),
        ("Consultant", "Consultant"),
    )
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Transgender", "Transgender")
    )
    marital_status_choice = (
        ("Single", "Single"),
        ("Marride", "Marride")
    )
    blood_group_choice = (
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("O+", "O+"),
        ("O-", "O-"),
        ("AB+", "AB+"),
        ("AB-", "AB-")
    )
    preferred_relationship_choice = (
        ("Father", "Father"),
        ("Mother", "Mother"),
        ("Spouse", "Spouse"),
        ("Son", "Son"),
        ("Daughter", "Daughter"),
        ("Other", "Other")
    )
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    employment_type = models.CharField(max_length=1000, null=True, blank=True, choices=employment_type_choice)
    profile_photo = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    father_hasband_name = models.CharField(max_length=255,null=True,blank=True)
    DOB = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    gender = models.CharField(max_length=1000, null=True, blank=True, choices=gender_choice)
    marital_status = models.CharField(max_length=1000, null=True, blank=True, choices=marital_status_choice)
    blood_group = models.CharField(max_length=1000, null=True, blank=True, choices=blood_group_choice)
    specially_abled = models.BooleanField(default=False)
    emargency_contact_person = models.CharField(max_length=255, null=True, blank=True)
    emargency_contact_phone = models.CharField(max_length=255, null=True, blank=True)
    preferred_relationship = models.CharField(max_length=1000, null=True, blank=True, choices=preferred_relationship_choice)
    permanent_house_no = models.CharField(max_length=200, null=True, blank=True)
    permanent_street_name_address = models.CharField(max_length=1000, null=True, blank=True)
    permanent_post_office = models.CharField(max_length=255, null=True, blank=True)
    permanent_district = models.CharField(max_length=255, null=True, blank=True)
    permanent_pin_code = models.CharField(max_length=1000, null=True, blank=True)
    permanent_state = models.CharField(max_length=255, null=True, blank=True)
    permanent_residing_since = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    permanent_currently_reside_at_same_address = models.BooleanField(default=False)
    current_house_no = models.CharField(max_length=200, null=True, blank=True)
    current_street_name_address = models.CharField(max_length=1000, null=True, blank=True)
    current_post_office = models.CharField(max_length=255, null=True, blank=True)
    current_district = models.CharField(max_length=255, null=True, blank=True)
    current_pin_code = models.CharField(max_length=1000, null=True, blank=True)
    current_state = models.CharField(max_length=255, null=True, blank=True)
    current_residing_since = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    current_currently_reside_at_same_address = models.BooleanField(default=False)




class EducationDetails(models.Model):
    degree_qualification_choice =(
        ("Below 10th", "Below 10th"),
        ("10th/ SSLC", "10th/ SSLC"),
        ("12th/ HSC", "12th/ HSC"),
        ("Under-graduate", "Under-graduate"),
        ("Graduate", "Graduate"),
        ("Post-Graduate", "Post-Graduate")
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    degree_qualification = models.CharField(max_length=1000, null=True, blank=True, choices=degree_qualification_choice)
    institute_name = models.CharField(max_length=255,null=True,blank=True)
    board_university = models.CharField(max_length=255, null=True, blank=True)
    percentage_GPA = models.DecimalField(max_digits = 5, decimal_places = 2,null=True,blank=False)
    passout_year = models.IntegerField(null=True,blank=True)
    # education_documents = models.FileField(upload_to=r'uploads/%Y/%m/%d/', null=True, blank=True)



class FamilyDetails(models.Model):
    spouse_gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    father_DOB = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    father_residing_with_you = models.BooleanField(default=False)
    mother_name = models.CharField(max_length=255, null=True, blank=True)
    mother_DOB = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    mother_residing_with_you = models.BooleanField(default=False)
    father_place_of_residence = models.CharField(max_length=1000,null=True,blank=True)
    father_insurance_persentage = models.DecimalField(max_digits = 5, decimal_places = 2,null=True,blank=False)
    mother_place_of_residence = models.CharField(max_length=1000, null=True, blank=True)
    mother_insurance_persentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False)
    spouse_name = models.CharField(max_length=255,null=True,blank=True)
    spouse_DOB = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    spouse_gender = models.CharField(max_length=1000, null=True, blank=True, choices=spouse_gender_choice)
    spouse_residing_with_you = models.BooleanField(default=False)
    spouse_place_of_residence = models.CharField(max_length=1000, null=True, blank=True)
    spouse_insurance_persentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False)
    children = models.BooleanField(default=False)
    # children_name = models.CharField(max_length=255,null=True,blank=True)
    # children_gender = models.CharField(max_length=1000, null=True, blank=True, choices=children_gender_choice)
    # children_place_of_residence = models.CharField(max_length=1000, null=True, blank=True)
    # children_insurance_persentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False)


class ChildrenDetails(models.Model):
    children_gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    children_name = models.CharField(max_length=255, null=True, blank=True)
    children_gender = models.CharField(max_length=1000, null=True, blank=True, choices=children_gender_choice)
    children_place_of_residence = models.CharField(max_length=1000, null=True, blank=True)
    children_insurance_persentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False)


class ChildrenAppuserMapping(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    children_id = models.ForeignKey(ChildrenDetails, on_delete=models.CASCADE)





class WorkExperience(models.Model):
    relationship_with_reporting_manager_choice = (
        ("Good", "Good"),
        ("Bad", "Bad"),
        ("Other", "Other")
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    work_experience_year = models.IntegerField(null=True,blank=True)
    work_experience_month = models.IntegerField(null=True, blank=True)
    currently_employment = models.BooleanField(default=False)
    company_name = models.CharField(max_length=1000,null=True,blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    joining_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    ctc = models.IntegerField(null=True,blank=True)
    company_address = models.CharField(max_length=1000,null=True,blank=True)
    employee_code = models.CharField(max_length=200,null=True,blank=True)
    reporting_manager = models.CharField(max_length=255, null=True, blank=True)
    relationship_with_reporting_manager = models.CharField(max_length=1000, null=True, blank=True, choices=relationship_with_reporting_manager_choice)
    previous_Work_experience = models.BooleanField(default=False)
    # exit_letter = models.FileField(upload_to=r'uploads/%Y/%m/%d/', null=True, blank=True)





class KYC(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    have_pan_number = models.BooleanField(default=False)
    pan_number = models.CharField(max_length=255,null=True,blank=True)
    # pan_card_file = models.FileField(upload_to=r'uploads/%Y/%m/%d/', null=True, blank=True)
    bank_account_number = models.CharField(max_length=255,null=True,blank=True)
    re_bank_account_number = models.CharField(max_length=255,null=True,blank=True)
    bank_name = models.CharField(max_length=1000,null=True, blank=True)
    branch_name = models.CharField(max_length=1000,null=True, blank=True)
    IFSC_code = models.CharField(max_length=200,null=True, blank=True)
    # bank_document = models.FileField(upload_to=r'uploads/%Y/%m/%d/', null=True, blank=True)
    internation_worker = models.BooleanField(default=True)
    country_of_origin = models.CharField(max_length=1000,null=True,blank=True)
    passport_number = models.CharField(max_length=255,null=True,blank=True)
    passport_validity_from = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    passport_validity_to = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    # passport_file = models.FileField(upload_to=r'uploads/%Y/%m/%d/', null=True, blank=True)



class EPF(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uan_number = models.CharField(max_length=255,null=True,blank=True)
    privious_pf_member_id = models.CharField(max_length=255,null=True,blank=True)
    exit_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    scheme_certificate_number = models.CharField(max_length=255,null=True,blank=True)
    pension_payment_order_number = models.CharField(max_length=255,null=True,blank=True)
    member_of_epf_scheme = models.BooleanField(default=False)
    member_of_ep_scheme = models.BooleanField(default=False)
    partA_provident_fund_scheme_demeed_cancelled = models.BooleanField(default=False)
    partA_father_mothe_depend_upon_me = models.BooleanField(default=False)
    partA_father_name = models.CharField(max_length=255,null=True,blank=True)
    partA_father_allocated_percentage = models.CharField(max_length=255, null=True, blank=True)
    partA_father_address = models.CharField(max_length=1000, null=True, blank=True)
    partA_mother_name = models.CharField(max_length=255,null=True,blank=True)
    partA_mother_address = models.CharField(max_length=1000, null=True, blank=True)
    partA_mother_allocated_percentage = models.CharField(max_length=255, null=True, blank=True)
    partA_spouse_name = models.CharField(max_length=255,null=True,blank=True)
    partA_spouse_address = models.CharField(max_length=1000,null=True,blank=True)
    partA_spouse_allocated_percentage = models.CharField(max_length=255, null=True, blank=True)
    partB_provident_fund_scheme_demeed_cancelled = models.BooleanField(default=False)
    partB_father_mothe_depend_upon_me = models.BooleanField(default=False)
    partB_spouse_name = models.CharField(max_length=255, null=True, blank=True)
    partB_spouse_allocated_percentage = models.CharField(max_length=255, null=True, blank=True)
    partB_spouse_address = models.CharField(max_length=1000, null=True, blank=True)





class ESIC(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    eligible_for_esic = models.BooleanField(default=False)
    insurance_name = models.CharField(max_length=1000,null=True,blank=True)
    employee_code_number = models.CharField(max_length=255,null=True,blank=True)
    select_nominee = models.CharField(max_length=1000,null=True,blank=True)
    branch_office_number = models.CharField(max_length=255,null=True,blank=True)
    despensary_name = models.CharField(max_length=1000,null=True,blank=True)


class AadharVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    aadhar_number = models.CharField(max_length=255,blank=False)
    isVerified = models.BooleanField(blank=False, default=False)





class Media(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=255,null=True,blank=True)
    file_url = models.TextField(null=True,blank=True)







