from django.urls import path

from adminUser.views import GetSalarySlipView, DeleteAppuserSalarySlipDataView
from recruiter.views import getPhoneNumberRegistered
from . import views as appUser_views
from .views import AppuserListByRecruiterId, AadharVerificationCreateView

urlpatterns = [
        path('personal/detail/', appUser_views.AppuserPersonaldetailsCreateView.as_view()),
        path('personal/detail/<int:pk>', appUser_views.AppuserPersonaldetailView.as_view()),
        path('education/detail/', appUser_views.AppuserEducationDetailCreateView.as_view()),
        path('education/detail/<int:pk>', appUser_views.AppuserEducationDetailView.as_view()),
        path('family/detail/', appUser_views.AppuserFamilyDetailCreateView.as_view()),
        path('get/family/detail/<int:pk>', appUser_views.AppuserFamilyDetailView.as_view()),
        path('get/child/detail/<int:pk>', appUser_views.AppuserChildrenList.as_view()),
        path('workexperience/detail/', appUser_views.AppuserWorkExperienceCreateView.as_view()),
        path('workexperience/detail/<int:pk>', appUser_views.AppuserWorkExperienceView.as_view()),
        path('KYC/detail/', appUser_views.AppuserKYCCreateView.as_view()),
        path('KYC/detail/<int:pk>', appUser_views.AppuserKYCDetailView.as_view()),
        path('EPF/detail/', appUser_views.AppuserEPFCreateView.as_view()),
        path('EPF/detail/<int:pk>', appUser_views.AppuserEPFDetailView.as_view()),
        path('ESIC/detail/', appUser_views.AppuserESICCreateView.as_view()),
        path('ESIC/detail/<int:pk>', appUser_views.AppuserESICDetailView.as_view()),
        path('get/appuser/list/<int:pk>',AppuserListByRecruiterId.as_view()),
        path('get/selary/slip/',GetSalarySlipView.as_view()),
        path("<phone>/", getPhoneNumberRegistered.as_view(), name="OTP Gen"),
        path("aadhar/verification/", AadharVerificationCreateView.as_view(), name="appuser_aadhar_verification"),
        path('get/documents/<int:pk>',appUser_views.GetUserDocuments.as_view()),
        path('delete/salary/slip/',DeleteAppuserSalarySlipDataView.as_view())

]