from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings

from django.core.files import File
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import DjangoUnicodeDecodeError, force_str
from django.utils import timezone
from django.shortcuts import get_list_or_404

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from datetime import datetime
import jwt
import requests
import tempfile

from gaggamagga.settings import get_secret
from .jwt_claim_serializer import CustomTokenObtainPairSerializer
from .serializers import (SignupSerializer,UserUpdateSerializer, PublicProfileSerializer,
LogoutSerializer, ProfileUpdateSerializer, ChangePasswordSerializer, SetNewPasswordSerializer, 
PasswordResetSerializer, LoginLogListSerializer, PrivateProfileSerializer)
from .models import User, ConfirmEmail, ConfirmPhoneNumber, Profile, LoggedIn, OauthId
from .utils import Util

class UserView(APIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == "PUT" or self.request.method == "DELETE":
            return [IsAuthenticated(),]
        return super(UserView, self).get_permissions()

    #회원가입
    @swagger_auto_schema(request_body=SignupSerializer, 
                    operation_summary="회원가입",  
                    responses={201 : '성공', 400 : '인풋값 에러', 500 : '서버 에러'})
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user = get_object_or_404(User, email=request.data["email"])

            secured_key = RefreshToken.for_user(user).access_token
            expired_at = datetime.fromtimestamp(secured_key['exp']).strftime("%Y-%m-%dT%H:%M:%S")

            ConfirmEmail.objects.create(secured_key=secured_key, expired_at=expired_at, user=user)

            frontend_site = "127.0.0.1:5501" 
            absurl = f'http://{frontend_site}/confrim_email.html?secured_key={str(secured_key)}'
            email_body = '안녕하세요!' + user.username +"고객님 이메일인증을 하시려면 아래 사이트를 접속해주세요 \n" + absurl
            message = {'email_body': email_body,'to_email':user.email, 'email_subject':'이메일 인증' }
            Util.send_email(message)

            return Response({"message":"회원가입이 되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #회원정보 수정
    @swagger_auto_schema(request_body=UserUpdateSerializer, 
                    operation_summary="회원정보 수정",  
                    responses={200 : '성공', 400 : '인풋값 에러', 404:'찾을 수 없음', 500 : '서버 에러'})
    def put(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserUpdateSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"회원 수정이 완료되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #회원 비활성화
    @swagger_auto_schema(operation_summary="회원 비활성화",
                    responses={200 : '성공', 403 : '접근 권한 에러', 500 : '서버에러'})
    def delete(self, request):
        user = get_object_or_404(User, id=request.user.id)
        user.withdraw = True
        user.withdraw_at = timezone.now()
        user.save()
        return Response({"message":"회원 비활성화가 되었습니다."}, status=status.HTTP_200_OK)

#로그인
class CustomTokenObtainPairView(TokenViewBase):
    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER

    @swagger_auto_schema(request_body=CustomTokenObtainPairSerializer,
                    operation_summary="로그인",
                    responses={200: '성공', 400: '인풋값 에러', 500: '서버에러'})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            #로그인 로그 저장
            user_ip= Util.get_client_ip(request)
            user = User.objects.get(username=request.data["username"])
            LoggedIn.objects.create(user=user, created_at=timezone.now(), update_ip=user_ip)

        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)        

class CustomTokenObtainPairView(CustomTokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

#로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=LogoutSerializer,
                    operation_summary="로그아웃",
                    responses={200 : '성공', 400 : '토큰 유효하지 않음', 401 : '인증 에러', 500 : '서버 에러'})
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"로그아웃 성공되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    secured_key_param_config = openapi.Parameter('secured_key', in_=openapi.IN_QUERY, description='Secured_key', type=openapi.TYPE_STRING)
    
    #이메일 인증 확인
    @swagger_auto_schema(manual_parameters=[secured_key_param_config],
                    operation_summary="이메일 인증 확인",
                    responses={200 : '성공', 400 : '토큰 유효하지 않음' , 404 : '찾을 수 없음' , 500 : '서버 에러'})
    def get(self, request):
        secured_key = request.GET.get('secured_key')
        try:
            payload = jwt.decode(secured_key, get_secret("SECRET_KEY"), algorithms=['HS256'])
            user = get_object_or_404(User, id=payload['user_id'])
            if not user.is_confirmed:
                user.is_confirmed = True
                user.save()
                return Response({'message':'성공적으로 인증이 되었습니다'}, status=status.HTTP_200_OK)
            return Response({'message':'이미 인증이 완료되었습니다.'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'message':'토큰이 만료되었습니다'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'message':'토큰이 유효하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

class ReSendEmailView(APIView):
    permission_classes = [IsAuthenticated]

    #이메일 재발송
    @swagger_auto_schema(operation_summary="이메일 재발송", 
                    responses={200 : '성공', 401 : '인증 에러', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def post(self, request):
        user = get_object_or_404(User, id=request.user.id)

        secured_key = RefreshToken.for_user(user).access_token
        expired_at = datetime.fromtimestamp(secured_key['exp']).strftime("%Y-%m-%dT%H:%M:%S")

        ConfirmEmail.objects.create(secured_key=secured_key, expired_at=expired_at, user=user)

        frontend_site = "127.0.0.1:5501" 
        absurl = f'http://{frontend_site}/confrim_email.html?secured_key={str(secured_key)}'
        email_body = '안녕하세요!' + user.username +"고객님 이메일인증을 하시려면 아래 사이트를 접속해주세요 \n" + absurl
        message = {'email_body': email_body,'to_email':user.email, 'email_subject':'이메일 인증' }
        Util.send_email(message)

        return Response({"message":"인증 이메일이 발송되었습니다. 확인부탁드립니다."}, status=status.HTTP_200_OK)

#아이디 찾기 휴대폰 sms 발송
class SendPhoneNumberView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_summary="아이디 찾기 휴대폰 sms 발송", 
                    responses={200 : '성공', 400 : '인풋값 에러', 500 : '서버 에러'})
    def post(self, request):
        try:
            phone_number = request.data["phone_number"]
            if not User.objects.filter(phone_number=phone_number).exists():
                return Response({'message': '등록된 휴대폰 번호가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(phone_number=phone_number)
            ConfirmPhoneNumber.objects.create(user=user)
            return Response({'message':'인증번호가 발송되었습니다. 확인부탁드립니다.'}, status=status.HTTP_200_OK)

        except:
            return Response({'message':'휴대폰 번호를 입력해주세요'}, status=status.HTTP_400_BAD_REQUEST)

#아이디 찾기 인증번호 확인
class ConfirmPhoneNumberView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_summary="아이디 찾기 휴대폰 sms 발송", 
                    responses={200 : '성공', 400 : '인풋값 에러', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def post(self, request):
        try:
            phone_number = request.data['phone_number']
            auth_number = request.data['auth_number']

            user = get_object_or_404(User, phone_number=phone_number)
            confirm_phone_number = ConfirmPhoneNumber.objects.filter(user=user).last()

            if confirm_phone_number.expired_at < timezone.now():
                return Response({'message': '인증 번호 시간이 지났습니다.'}, status=status.HTTP_400_BAD_REQUEST)

            if confirm_phone_number.auth_number != int(auth_number):
                return Response({'message': '인증 번호가 틀립니다. 다시 입력해주세요'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message':f'회원님의 아이디는 {user.username}입니다.'}, status=status.HTTP_200_OK)
        
        except:
            return Response({'message': '인증번호를 확인해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

class PrivateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    #개인 프로필
    @swagger_auto_schema(operation_summary="개인 프로필", 
                    responses={200 : '성공',  404 : '찾을 수 없음', 500 : '서버 에러'}) 
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = PrivateProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #프로필 수정
    @swagger_auto_schema(request_body=ProfileUpdateSerializer, 
                    operation_summary="프로필 수정", 
                    responses={200 : '성공',  400 : '인풋값 에러', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def put(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileUpdateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"프로필 수정이 완료되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#공개 프로필 
class PublicProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="공개 프로필", 
                    responses={200 : '성공',  404 : '찾을 수 없음', 500 : '서버 에러'}) 
    def get(self, request, nickname):
        profile = get_object_or_404(Profile, nickname=nickname)
        serializer = PublicProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

#로그인 로그기록
class LoginLogListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="로그인 로그기록", 
                    responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'}) 
    def get(self, request):
        logged_in = get_list_or_404(LoggedIn, user=request.user)[:10]
        serializer = LoginLogListSerializer(logged_in, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    #비밀번호 변경
    @swagger_auto_schema(request_body=ChangePasswordSerializer, 
                    operation_summary="비밀번호 변경", 
                    responses={200 : '성공', 201 : '인증 에러', 400 :'인풋값 에러', 401 : '인증 에러', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def put(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = ChangePasswordSerializer(user, data=request.data, context={'request': request}) 
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"비밀번호 변경이 완료되었습니다! 다시 로그인해주세요."} , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#비밀번호 찾기(이메일 전송)
class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=PasswordResetSerializer, 
                    operation_summary="비밀번호 찾기", 
                    responses={200 : '성공', 400 : '인풋값 에러', 500 : '서버 에러'})
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({"message":"비밀번호 재설정 이메일을 발송했습니다. 확인부탁드립니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#비밀번호 재설정 토큰 확인
class PasswordTokenCheckView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_summary="비밀번호 재설정 토큰 확인", 
                    responses={200 : '성공', 401 : '링크 유효하지 않음', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"message":"링크가 유효하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({"message":"링크가 유효하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

#비밀번호 재설정
class SetNewPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=SetNewPasswordSerializer, 
                    operation_summary="비밀번호 재설정",
                    responses={200 : '성공', 400 : '인풋값 에러', 500 : '서버 에러'})
    def put(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message":"비밀번호 재설정 완료"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#비밀번호 변경일시 만료되면 변경
class ExpiredPasswordChage(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="유저 비밀번호 만료",
                    responses={200 : '성공', 401 : '인증에러', 403 : '접근 권한 에러', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if user.password_expired == True:
            return Response({"message":"비밀번호 만료일이 지났습니다. 비밀번호를 변경해주세요."}, status=status.HTTP_200_OK)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(operation_summary="비밀번호 다음에 변경",
                    responses={200 : '성공' , 401 : '인증에러', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def post(self, request):
        user = get_object_or_404(User, id=request.user.id)
        user.password_expired = False
        user.last_password_changed = timezone.now()
        user.save()
        return Response({"message":"비밀번호 다음에 변경하기"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ChangePasswordSerializer, 
                    operation_summary="비밀번호 인증 만료 시 변경", 
                    responses={200 : '성공', 400 : '인풋값 에러', 401 :'인증 에러', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def put(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = ChangePasswordSerializer(user, data=request.data, context={'request': request}) 
        if serializer.is_valid():
            serializer.save()
            user.password_expired = False
            user.save()
            return Response({"message":"비밀번호 변경이 완료되었습니다!"} , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#팔로우 
class ProcessFollowView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="팔로우", 
                        responses={ 200 : '성공', 404:'찾을 수 없음', 500:'서버 에러'})
    def post(self, request, nickname):
        you = get_object_or_404(Profile, nickname=nickname)
        me = request.user.user_profile
        if me in you.followers.all():
            you.followers.remove(me)
            return Response({"message":"팔로우를 했습니다."}, status=status.HTTP_200_OK)
        else:
            you.followers.add(me)
            return Response({"message":"팔로우를 취소했습니다."}, status=status.HTTP_200_OK)

#카카오 로그인
class KakaoLoginView(APIView):
    permission_classes = [AllowAny]
        
    @swagger_auto_schema(operation_summary="카카오 소셜 로그인", 
                        responses={ 200 : '성공', 400: '잘못된 요청', 500:'서버 에러'})
    def post(self, request):
        try:
            code = request.data.get('code')
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": get_secret("SOCIAL_AUTH_KAKAO_CLIENT_ID"),
                    "redirect_uri": "http://127.0.0.1:5501",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            
            user_data = user_data.json()

            kakao_email = user_data.get('kakao_account')['email']
            kakao_nickname = user_data.get('properties')['nickname']
            kakao_profile_image = user_data.get('properties')['profile_image']

            try:
                user = User.objects.get(email=kakao_email)
                social_user = OauthId.objects.filter(user=user).first()
                if social_user:
                    if social_user.provider !="kakao":
                        return Response({"error":"카카오로 가입한 유저가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
                    
                    user.withdraw = False
                    user.save()
                    
                    refresh = RefreshToken.for_user(user)
                    return Response({'refresh': str(refresh), 'access':str(refresh.access_token)}, status=status.HTTP_200_OK)
                
                if social_user is None:
                    return Response({"error":"이메일이 존재하지만 , 소셜유저가 아닙니다"}, status=status.HTTP_400_BAD_REQUEST)
                
            except User.DoesNotExist:
                new_user = User.objects.create(username=kakao_nickname, email=kakao_email)
                new_user.set_unusable_password()
                new_user.save()
                
                profile = Profile.objects.create(nickname=kakao_nickname, user=new_user)
                OauthId.objects.create(provider="kakao", access_token=access_token, user=new_user)
                
                util_image = Util.profile_image_download(kakao_profile_image)
                profile.profile_image.save(util_image["file_name"], File(util_image["temp_image"]))
                
                refresh = RefreshToken.for_user(new_user)
                
                return Response({'refresh': str(refresh), 'access':str(refresh.access_token)}, status=status.HTTP_200_OK)
            
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)