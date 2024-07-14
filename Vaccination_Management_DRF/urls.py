
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('patient/', include('patient.urls')),
    path('doctor/', include('doctor.urls')),
    path('vaccine-campaign/', include('vaccine_campaign.urls')),
    path('user/', include('user.urls')),
]
