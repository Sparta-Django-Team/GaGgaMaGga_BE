from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path

from . import views

urlpatterns = [
    #User
    path('', views.UserView.as_view(), name='user'),
    path('email-confirm/', views.ConfirmEmailView.as_view(), name='confirm_email'),
    path('email-resend/', views.ReSendEmailView.as_view(), name='reconfirm_email'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('phone-number-send/', views.SendPhoneNumberView.as_view(), name='send_phone_number'),
    path('phone-number-confirm/', views.ConfirmPhoneNumberView.as_view(), name='confirm_phone_number'),
<<<<<<< HEAD
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    
=======
    path('profile/', views.PrivateProfileView.as_view(), name='private_profile'),
    path('profile/<str:nickname>/', views.PublicProfileView.as_view(), name='public_profile'),
    path('log/', views.LoginLogListView.as_view(), name='login_log'),
    path("kakao/", views.KakaoLogIn.as_view()),

>>>>>>> c338295891312c341f1fe5ed232a361ddbea9f42
    #Password
    path('password-change/', views.ChangePasswordView.as_view(), name='change_password_view'),
    path('password-reset-email/', views.PasswordResetView.as_view(),name="password_reset_email"),
    path('password-reset/<uidb64>/<token>/',views.PasswordTokenCheckView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.SetNewPasswordView.as_view(), name='password_reset_complete'),
    path('password-expired-change/', views.ExpiredPasswordChage.as_view(), name='password_expired_change'),
] 