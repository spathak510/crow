from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from adminUser import views
from adminUser.views import PasswordResetView, PasswordResetConfirmView, offerletterView, get_pdf, \
    GetAllAppUserlist, GetAllRecruiterlist, GetAllClientlist, GetAllAdminusertlist, salarySlipCreation, \
    ClientRecruiterMappingByAdmin, GetClientRecruiterMappingData, ClientRecruiterUnMapping, ClientUpdateView, \
    RecruiterUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^password/reset/$', PasswordResetView.as_view(),name='rest_password_reset'),
    path(r'password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path("account/", include('allauth.urls')),
    url(r'^password/change/$', views.PasswordChangeView.as_view(),name='rest_password_change'),
    path('recruiter/', include('recruiter.urls')),
    path('appuser/', include('appUser.urls')),
    path('offerletter/view/',offerletterView,name='crowning_offerletter'),
    path('issue/offerletter/',get_pdf,name="offerletter_upload"),
    path('upload/salary/file/',salarySlipCreation.as_view()),
    path('get/all/appuser/list/',GetAllAppUserlist.as_view()),
    path('get/all/recruiter/list/',GetAllRecruiterlist.as_view()),
    path('get/all/client/list/',GetAllClientlist.as_view()),
    path('get/all/adminuser/list/',GetAllAdminusertlist.as_view()),
    path('client/recruiter/mapping/',ClientRecruiterMappingByAdmin.as_view()),
    path('get/client/recruiter/mapping/',GetClientRecruiterMappingData.as_view()),
    path('client/recruiter/unmapping/',ClientRecruiterUnMapping.as_view()),
    path('client/update/',ClientUpdateView.as_view()),
    path('recruiter/update/',RecruiterUpdateView.as_view())
    # path('upload/salary/file/',salarySlipCreation,name='upload_salary_slip_document')
]
