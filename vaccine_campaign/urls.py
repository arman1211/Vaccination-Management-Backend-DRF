from rest_framework.routers import DefaultRouter
from .views import VaccineReviewPostView, VaccineCampaignViewSet,VaccineDoseBookingViewSet,VaccineReviewViewSet,VaccineDoseBookingCreateView,VaccineCampaignDetailsViewSet
from django.urls import path,include

router = DefaultRouter()

router.register('list',VaccineCampaignViewSet)
router.register('booking',VaccineDoseBookingViewSet)
router.register('review',VaccineReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lists/<int:pk>/', VaccineCampaignDetailsViewSet.as_view(), name='vaccine-campaign-detail'),
    path('post/', VaccineDoseBookingCreateView.as_view(), name='vaccine-dose-create'),
    path('review/post/', VaccineReviewPostView.as_view(), name='vaccine-review-post'),
]
