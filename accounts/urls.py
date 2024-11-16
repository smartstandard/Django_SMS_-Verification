from django.urls import path
from .views import send_verification_code, verify_code

urlpatterns = [
    path('send-code/', send_verification_code, name='send_code'),
    path('verify-code/', verify_code, name='verify_code'),
]