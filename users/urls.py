from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path

from . import views

urlpatterns = [
    # User
    path('', views.UserView.as_view(), name='user_view'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair_view'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('logout/', views.LogoutView.as_view(), name='logout_view'),
    path("kakao/", views.KakaoLoginView.as_view(), name='kakao_login_view'),
    
    # Email
    path('email-confirm/', views.ConfirmEmailView.as_view(), name='confirm_email_view'),
    path('email-resend/', views.ReSendEmailView.as_view(), name='resend_email_view'),
    
    # Phone_number
    path('phone-number-send/', views.SendPhoneNumberView.as_view(), name='send_phone_number_view'),
    path('phone-number-confirm/', views.ConfirmPhoneNumberView.as_view(), name='confirm_phone_number_view'),
    
    # Profile
    path('profiles/', views.PrivateProfileView.as_view(), name='private_profile_view'),
    path('profiles/<str:nickname>/', views.PublicProfileView.as_view(), name='public_profile_view'),
    
    # Log
    path('logs/', views.LoginLogListView.as_view(), name='login_log_view'),
    
    # Follow
    path('follow/<str:nickname>/', views.ProcessFollowView.as_view(), name='process_follow_view'),
    
    # Password
    path('password-change/', views.ChangePasswordView.as_view(), name='change_password_view'),
    path('password-reset-email/', views.PasswordResetView.as_view(),name="password_reset_email_view"),
    path('password-reset/<uidb64>/<token>/',views.PasswordTokenCheckView.as_view(), name='password_reset_confirm_view'),
    path('password-reset-complete/', views.SetNewPasswordView.as_view(), name='password_reset_complete_view'),
    path('password-expired-change/', views.ExpiredPasswordChage.as_view(), name='password_expired_change_view'),
] 