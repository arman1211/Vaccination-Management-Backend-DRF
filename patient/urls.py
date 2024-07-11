from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import PatientView,PatientRegisterView,DoctorView,DoctorRegisterView,activate

router = DefaultRouter()

router.register('patient/list', PatientView)
router.register('doctor/list', DoctorView)

urlpatterns = [
    path('',include(router.urls)),
    path('patient/register/', PatientRegisterView.as_view(), name='patient-register'),
    path('doctor/register/', DoctorRegisterView.as_view(), name='patient-register'),
    path('patient/active/<uid64>/<token>/', activate, name = 'activate')
]
