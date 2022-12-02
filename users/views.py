from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

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
from .serializers import SignupSerializer
from .models import User, ConfirmEmail, ConfirmPhoneNumber
from .utils import Util

class UserView(APIView):
    permission_classes = [AllowAny]

    #회원가입
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            user = get_object_or_404(User, email=request.data["email"])
            
            secured_key = RefreshToken.for_user(user).access_token
            expired_at = datetime.fromtimestamp(secured_key['exp']).strftime("%Y-%m-%dT%H:%M:%S")
            
            ConfirmEmail.objects.create(secured_key=secured_key, expired_at=expired_at, user=user)
            
            frontend_site = "127.0.0.1:5500" 
            absurl = f'http://{frontend_site}/confrim_email.html?secured_key={str(secured_key)}'
            email_body = '안녕하세요!' + user.username +"고객님 이메일인증을 하시려면 아래 사이트를 접속해주세요 \n" + absurl
            message = {'email_body': email_body,'to_email':user.email, 'email_subject':'이메일 인증' }
            Util.send_email(message)
            
            return Response({"message":"회원가입이 되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#로그인
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
