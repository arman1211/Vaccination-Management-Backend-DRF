from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import PatientView,PatientRegisterView,activate,PaymentDetailView,PaymentDetailsByPatientView, PatientUpdateView,PasswordUpdateView,InitiatePaymentView, PaymentSuccessView, PaymentFailView, PaymentCancelView

router = DefaultRouter()

router.register('list', PatientView)

urlpatterns = [
    path('',include(router.urls)),
    path('register/', PatientRegisterView.as_view(), name='patient-register'),
    path('active/<uid64>/<token>/', activate, name = 'activate'),
     path('update-patient/<int:id>', PatientUpdateView.as_view(), name='update'),
     path('update-password/<int:id>', PasswordUpdateView.as_view(), name='update-password'),

     path('payment/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('payment/fail/', PaymentFailView.as_view(), name='payment-fail'),
    path('payment/cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
    path('payment/detail/<str:transaction_id>', PaymentDetailView.as_view(), name='payment-view'),
    path('payment/details/<int:patientId>', PaymentDetailsByPatientView.as_view(), name='payment-view-patient'),
]
