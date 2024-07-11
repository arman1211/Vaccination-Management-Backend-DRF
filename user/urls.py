from .views import UserLoginApiView,UserLogoutView,UserListView,PatientRegisterView,DoctorRegisterView
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('list',UserListView)

urlpatterns = [
    path('',include(router.urls)),
    path('login/',UserLoginApiView.as_view(), name='login'),
    path('logout/',UserLogoutView.as_view(), name='logout'),
    path('register/patient/', PatientRegisterView.as_view(), name='patient-register'),
    path('register/doctor/', DoctorRegisterView.as_view(), name='doctor-register'),
]
