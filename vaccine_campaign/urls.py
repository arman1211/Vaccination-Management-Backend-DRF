from rest_framework.routers import DefaultRouter
from .views import generate_pdf_report,DeleteVaccineDoseBooking,VaccineDoseBookingByPatient, UpdateVaccineCampaignView,DeleteVaccineCampaignView, VaccineReviewPostView, CompleteDoseView, VaccineCampaignViewSet,VaccineDoseBookingViewSet,VaccineReviewViewSet,VaccineDoseBookingCreateView,VaccineCampaignDetailsViewSet
from django.urls import path,include

router = DefaultRouter()

router.register('list',VaccineCampaignViewSet)
router.register('booking',VaccineDoseBookingViewSet)
router.register('review',VaccineReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lists/<int:pk>/', VaccineCampaignDetailsViewSet.as_view(), name='vaccine-campaign-detail'),
    path('bookings/<int:patient_id>/', VaccineDoseBookingByPatient.as_view(), name='vaccinedose'),
    path('complete/<int:id>/', CompleteDoseView.as_view(), name='vaccine-complete'),
    path('post/', VaccineDoseBookingCreateView.as_view(), name='vaccine-dose-create'),
    path('review/post/', VaccineReviewPostView.as_view(), name='vaccine-review-post'),
     path('edit/<int:id>/', UpdateVaccineCampaignView.as_view(), name='edit-campaign'),
    path('delete/<int:id>/', DeleteVaccineCampaignView.as_view(), name='delete-campaign'),
    path('booking/delete/<int:id>/', DeleteVaccineDoseBooking.as_view(), name='delete-booking'),
     path('vaccine-dose-report/<int:id>/', generate_pdf_report, name='generate_pdf_report'),
]
