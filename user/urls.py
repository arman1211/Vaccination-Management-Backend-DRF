from .views import UserLoginApiView,UserLogoutView
from django.urls import path




urlpatterns = [
    
    path('login/',UserLoginApiView.as_view(), name='login'),
    path('logout/',UserLogoutView.as_view(), name='logout')
]
