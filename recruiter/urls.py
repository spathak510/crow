from django.urls import path
from . import views as recruiter_views
from .views import ClientListByAdminuserId, ClientLocationMappingCreateView, \
    RecruiterListByAdminuserId, ClientLocationList, ClientLocationDeleteView, ClientLocationUpdateView

urlpatterns = [
    path('offerletter/', recruiter_views.AppuserOfferletterCreateView.as_view()),
    path('client/list/<int:pk>',ClientListByAdminuserId.as_view()),
    path('client/location/mapping/',ClientLocationMappingCreateView.as_view()),
    path('list/<int:pk>',RecruiterListByAdminuserId.as_view()),
    path('clint/location/list/<int:pk>',ClientLocationList.as_view()),
    path('clint/location/delete/<int:pk>',ClientLocationDeleteView.as_view()),
    path('client/location/update/',ClientLocationUpdateView.as_view())
]