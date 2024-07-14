from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import PatientView,PatientRegisterView,activate, PatientUpdateView,PasswordUpdateView

router = DefaultRouter()

router.register('list', PatientView)

urlpatterns = [
    path('',include(router.urls)),
    path('register/', PatientRegisterView.as_view(), name='patient-register'),
    path('active/<uid64>/<token>/', activate, name = 'activate'),
     path('update-patient/<int:id>', PatientUpdateView.as_view(), name='update'),
     path('update-password/<int:id>', PasswordUpdateView.as_view(), name='update-password'),
]
