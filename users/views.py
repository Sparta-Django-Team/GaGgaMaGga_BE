from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import DjangoUnicodeDecodeError, force_str
from django.conf import settings
from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema

from datetime import datetime
import jwt

from .jwt_claim_serializer import CustomTokenObtainPairSerializer
from .serializers import SignupSerializer, ProfileSerializer
from .models import User, ConfirmEmail, ConfirmPhoneNumber
from .utils import Util

class UserView(APIView):
    permission_classes = [AllowAny]

    #회원가입
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"회원가입이 되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #회원 비활성화
    def delete(self, request):
        user = User.objects.filter(id=request.user.id)
        if user:
            user.update(withdraw="True", withdraw_at=str(timezone.now()))
            return Response({"message":"회원 비활성화가 되었습니다."}, status=status.HTTP_200_OK)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

class ProfileView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [AllowAny]

    #프로필 
    def get(self, request):
        print(request.META)
        user = get_object_or_404(User, id=request.user.id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#로그인
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
