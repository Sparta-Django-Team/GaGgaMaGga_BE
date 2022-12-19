from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MaxValueValidator, validate_image_file_extension, validate_ipv46_address

from django.utils import timezone

from gaggamagga.settings import get_secret

import base64
import hashlib
import hmac
import time
import requests
from random import randint

class UserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None):
        
        if not username:
            raise ValueError('아이디를 입력해주세요.')
        
        if not email:
            raise ValueError('이메일을 입력해주세요.')
        
        if not phone_number:
            raise ValueError('휴대폰 번호를 입력해주세요.')
        
        user = self.model(
            username=username,
            email=email, 
            phone_number=phone_number
        )
        
        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password=None):
        user = self.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField('아이디', max_length=15, unique=True, error_messages={"unique": "이미 사용중인 아이디 이거나 탈퇴한 아이디입니다."})
    email = models.EmailField('이메일', max_length=255, unique=True, error_messages={"unique": "이미 사용중인 이메일 이거나 탈퇴한 이메일입니다."})
    phone_number = models.CharField('휴대폰 번호', max_length = 11, blank=True)
    account_lock_count = models.IntegerField('로그인 제한 횟수', default=0)
    account_lock_time = models.DateTimeField('로그인 제한 시간',null=True)
    is_admin = models.BooleanField('관리자', default=False)
    is_active = models.BooleanField('로그인 가능', default=True)
    is_confirmed = models.BooleanField('이메일 확인', default=False)
    withdraw = models.BooleanField('회원 비활성화', default=False)
    password_expired = models.BooleanField('비밀번호 만료', default=False)
    last_password_changed = models.DateTimeField('비밀번호 마지막 변경일', auto_now=True)
    created_at = models.DateTimeField('계정 생성일', auto_now_add=True)
    withdraw_at = models.DateTimeField('계정 탈퇴일', null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number',]

    def __str__(self):
        return f"[아이디]{self.username}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

# 이메일 확인 
class ConfirmEmail(models.Model):
    secured_key = models.CharField('시크릿 키', max_length=255, default=0)
    expired_at = models.DateTimeField('만료일', auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="회원")
    
    def __str__(self):
        return f"[이메일]{self.user.email}"

# 휴대폰 번호 확인
class ConfirmPhoneNumber(models.Model): 
    auth_number = models.IntegerField('인증 번호', default=0, validators=[MaxValueValidator(9999)])
    expired_at = models.DateTimeField('만료일',)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="회원")
    
    def save(self, *args, **kwargs):
        self.auth_number = randint(1000, 10000)
        self.expired_at = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)
        self.send_sms()
    
    def send_sms(self):
        timestamp = str(int(time.time() * 1000))
        access_key =  get_secret("NAVER_ACCESS_KEY_ID")
        secret_key = bytes( get_secret("NAVER_SECRET_KEY"), "UTF-8")
        service_id = get_secret("SERVICE_ID")
        method = "POST"
        uri = f"/sms/v2/services/{service_id}/messages"
        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, "UTF-8")
        signing_key = base64.b64encode(
            hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
        )
        
        url = f"https://sens.apigw.ntruss.com/sms/v2/services/{service_id}/messages"
        
        data = {
            "type": "SMS",
            "from": f'{get_secret("FROM_PHONE_NUMBER")}',
            "content": f"[가까? 마까?] 인증 번호 [{self.auth_number}]를 입력해주세요. (5분 제한시간)",
            "messages": [{"to": f"{self.user.phone_number}"}],
        }

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": access_key,
            "x-ncp-apigw-signature-v2": signing_key,
        }
        
        requests.post(url, json=data, headers=headers)

    def __str__(self):
        return f"[휴대폰 번호]{self.user.phone_number}"

# 로그 기록
class LoggedIn(models.Model):
    update_ip = models.GenericIPAddressField('로그인한 IP', null=True, validators=[validate_ipv46_address])
    created_at = models.DateTimeField('로그인 기록', auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="회원")

    def __str__(self):
        return f"[아이디]{self.user.username}, [접속 기록]{self.created_at}"

    class Meta:
        ordering = ['-created_at']

# 소셜 로그인
class OauthId(models.Model):
    access_token = models.CharField('토큰', max_length=255)
    provider = models.CharField('구분자', max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="회원")
    
    def __str__(self):
        return f"[아이디]{self.user.username}, [소셜 도메인]{self.provider}"

# 프로필
class Profile(models.Model):
    profile_image = models.ImageField('프로필 사진', default='default_profile_pic.png', upload_to='profile_pics', validators=[validate_image_file_extension])
    nickname = models.CharField('닉네임', max_length=10, null=True, unique=True, error_messages={"unique": "이미 사용중인 닉네임 이거나 탈퇴한 닉네임입니다."})
    intro = models.CharField('자기소개', max_length=100, null=True)
    review_cnt = models.PositiveIntegerField('리뷰수', default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="회원", related_name='user_profile')
    
    followings = models.ManyToManyField('self', symmetrical=False, blank=True, related_name= 'followers')

    def __str__(self):
        return f"[아이디]{self.user.username}, [닉네임]{self.nickname}"

    @property
    def review_count_add(self):
        self.review_cnt +=1
        self.save()

    @property
    def review_count_remove(self):
        self.review_cnt -=1
        self.save()
