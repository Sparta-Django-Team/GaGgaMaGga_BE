from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('', views.UserView.as_view(), name='user'),
    path('email-confirm/', views.ConfirmEmailView.as_view(), name='confirm_email'),
    path('email-resend/', views.ReSendEmailView.as_view(), name='reconfirm_email'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('phone-number-send/', views.SendPhoneNumberView.as_view(), name='send_phone_number'),
    path('phone-number-confirm/', views.ConfirmPhoneNumberView.as_view(), name='confirm_phone_number'),
]