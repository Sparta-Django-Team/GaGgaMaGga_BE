from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MaxValueValidator
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
    
#이메일 확인 
class ConfirmEmail(models.Model):
    secured_key = models.CharField('시크릿 키', max_length=255, default=0)
    expired_at = models.DateTimeField('만료일', auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="회원")
    
    def __str__(self):
        return f"[이메일]{self.user.email}"