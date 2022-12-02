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

#로그인
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    #이메일 인증 확인
    def get(self, request):
        secured_key = request.GET.get('secured_key')
        
        try:
            payload = jwt.decode(secured_key, settings.SECRET_KEY)
            user = get_object_or_404(User, id=payload['user_id'])
            if not user.is_confirm:
                user.is_confirm = True
                user.save()
            return Response({'message':'성공적으로 인증이 되었습니다'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'message':'토큰이 만료되었습니다'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'message':'토큰이 유효하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

class ReSendEmailView(APIView):
    permission_classes = [IsAuthenticated]
    
    #이메일 재발송
    def post(self, request):
        user = get_object_or_404(User, id=request.user.id)
        
        secured_key = RefreshToken.for_user(user).access_token
        expired_at = datetime.fromtimestamp(secured_key['exp']).strftime("%Y-%m-%dT%H:%M:%S")
        
        ConfirmEmail.objects.create(secured_key=secured_key, expired_at=expired_at, user=user)
        
        frontend_site = "127.0.0.1:5500" 
        absurl = f'http://{frontend_site}/confrim_email.html?secured_key={str(secured_key)}'
        email_body = '안녕하세요!' + user.username +"고객님 이메일인증을 하시려면 아래 사이트를 접속해주세요 \n" + absurl
        message = {'email_body': email_body,'to_email':user.email, 'email_subject':'이메일 인증' }
        Util.send_email(message)
        
        return Response({"message":"인증 이메일이 발송되었습니다. 확인부탁드립니다."}, status=status.HTTP_201_CREATED)
class ProfileView(APIView):
    permission_classes = [AllowAny]

    #프로필 
    def get(self, request):
        print(request.META)
        user = get_object_or_404(User, id=request.user.id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReSendEmailView(APIView):
    permission_classes = [IsAuthenticated]
    
    #이메일 재발송
    def post(self, request):
        user = get_object_or_404(User, id=request.user.id)
        
        secured_key = RefreshToken.for_user(user).access_token
        expired_at = datetime.fromtimestamp(secured_key['exp']).strftime("%Y-%m-%dT%H:%M:%S")
        
        ConfirmEmail.objects.create(secured_key=secured_key, expired_at=expired_at, user=user)
        
        frontend_site = "127.0.0.1:5500" 
        absurl = f'http://{frontend_site}/confrim_email.html?secured_key={str(secured_key)}'
        email_body = '안녕하세요!' + user.username +"고객님 이메일인증을 하시려면 아래 사이트를 접속해주세요 \n" + absurl
        message = {'email_body': email_body,'to_email':user.email, 'email_subject':'이메일 인증' }
        Util.send_email(message)
        
        return Response({"message":"인증 이메일이 발송되었습니다. 확인부탁드립니다."}, status=status.HTTP_201_CREATED)

