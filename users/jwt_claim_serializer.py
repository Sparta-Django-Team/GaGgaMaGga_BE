from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework import serializers, exceptions

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .utils import Util
from .models import User, BlockedCountryIP


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class = RefreshToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {self.username_field: attrs[self.username_field], "password": attrs["password"],}

        try:
            authenticate_kwargs["request"] = self.context["request"]

        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        try:
            username = attrs[self.username_field]
            self.target_user = User.objects.get(username=username)
            self.is_active = self.target_user.is_active
            self.withdraw = self.target_user.withdraw

            account_lock_count = self.target_user.account_lock_count

            # account_lock_count counting
            if self.user == None:
                self.target_user.account_lock_count += 1
                self.target_user.save()

            # account_lock_count 4이면 잠금
            if account_lock_count == 4:
                self.target_user.is_active = False
                self.target_user.account_lock_time = timezone.now()
                self.target_user.save()

            # is_active False 제한 시간 확인 후 True
            self.now_today_time = timezone.now()

            if self.is_active == False:
                target_user_lock_time = (self.target_user.account_lock_time + timezone.timedelta(minutes=3))

                if self.now_today_time >= target_user_lock_time:
                    self.target_user.is_active = True
                    self.target_user.account_lock_count = 0
                    self.target_user.save()

            # (회원비활성화) withdraw True이면 로그인 시 False
            if self.withdraw == True:
                self.target_user.withdraw = False
                self.target_user.save()

        except:
            pass

        if User.objects.filter(username=username).exists():

            # is_active False 계정잠금
            if self.is_active == False:
                raise serializers.ValidationError(detail={"error": "로그인 시도가 너무 많습니다. 3분 후 다시 시도해 주세요."})

            # IP 국가코드 차단 확인
            user_ip = Util.get_client_ip(self.context.get("request"))
            country = Util.find_ip_country(user_ip)
            if BlockedCountryIP.objects.filter(user=self.target_user, country=country).exists():
                raise serializers.ValidationError(detail={"error": "해당 IP를 차단한 계정입니다."})

        # login error
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(detail={"error": "아이디와 비밀번호를 확인해주세요."})

        # login token
        refresh = self.get_token(self.user)

        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return {"access": attrs["access"], "refresh": attrs["refresh"]}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["nickname"] = user.user_profile.nickname
        token["review_cnt"] = user.user_profile.review_cnt
        token["password_expired"] = user.password_expired
        token["is_admin"] = user.is_admin

        return token