from django.urls import path
from .api import AllUsersAPIView, ByIdUserAPIView, RegisterUserAPIView, AcceptEmailVerificationAPIView, \
    AcceptPhoneVerificationAPIView

urlpatterns = [
    path('profile/', AllUsersAPIView.as_view(), name='find-all-users'),
    path('profile/<str:id>/', ByIdUserAPIView.as_view(), name='find-user-profile-by-id'),
    path('email-verification/<str:code>/', AcceptEmailVerificationAPIView.as_view(), name='accept-email-verification'),
    path('phone-verification/<str:code>/', AcceptPhoneVerificationAPIView.as_view(), name='accept-phone-verification'),
    path('signup/', RegisterUserAPIView.as_view(), name='register-user'),
]
