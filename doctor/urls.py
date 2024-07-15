from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import DoctorView,DoctorRegisterView,activate,DoctorUpdateView

router = DefaultRouter()

router.register('list', DoctorView)

urlpatterns = [
    path('',include(router.urls)),
    path('register/', DoctorRegisterView.as_view(), name='patient-register'),
    path('active/<uid64>/<token>/', activate, name = 'activate'),
    path('update-doctor/<int:id>', DoctorUpdateView.as_view(), name='update-doctor'),
]
