
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('patient/', include('patient.urls')),
    path('doctor/', include('doctor.urls')),
    path('vaccine-campaign/', include('vaccine_campaign.urls')),
    path('user/', include('user.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)