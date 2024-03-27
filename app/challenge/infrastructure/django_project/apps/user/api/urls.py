from django.urls import path
from .api import AllUsersAPIView, ByIdUserAPIView, RegisterUserAPIView

urlpatterns = [
    path('profile/', AllUsersAPIView.as_view(), name='find-all-users'),
    path('profile/<str:id>/', ByIdUserAPIView.as_view(), name='find-user-profile-by-id'),
    path('signup/', RegisterUserAPIView.as_view(), name='register-user'),
]
