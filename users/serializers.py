from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str

import re

from .models import User, Profile
from .utils import Util

#회원가입 serializer
class SignupSerializer(serializers.ModelSerializer):
    repassword= serializers.CharField(error_messages={'required':'비밀번호를 입력해주세요.', 'blank':'비밀번호를 입력해주세요.', 'write_only':True})    
    term_check = serializers.BooleanField(error_messages={'required':'약관동의를 확인해주세요.', 'blank':'약관동의를 확인해주세요.', 'write_only':True})
    
    class Meta:
        model = User
        fields = ('username' ,'password', 'repassword', 'phone_number', 'email', 'term_check',)
        extra_kwargs = {
                        'username': {
                        'error_messages': {
                        'required': '아이디를 입력해주세요.',
                        'blank':'아이디를 입력해주세요',}},
                        
                        'password':{'write_only':True,
                        'error_messages': {
                        'required':'비밀번호를 입력해주세요.',
                        'blank':'비밀번호를 입력해주세요.',}},
                        
                        'email': {
                        'error_messages': {
                        'required': '이메일을 입력해주세요.',
                        'invalid': '알맞은 형식의 이메일을 입력해주세요.',
                        'blank':'이메일을 입력해주세요.',}},
                        
                        'phone_number':{
                        'error_messages':{
                        'required': '휴대폰 번호를 입력해주세요.',}}}

    def validate(self, data):
        PASSWORD_VALIDATION = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,16}"
        PASSWORD_PATTERN = r"(.)\1+\1"
        USERNAME_VALIDATION = r'^[A-Za-z0-9]{6,20}$'
        
        username = data.get('username')
        phone_number = data.get('phone_number')
        password = data.get('password')
        repassword = data.get('repassword')
        term_check = data.get('term_check')
        
        
        #아이디 유효성 검사
        if not re.search(USERNAME_VALIDATION, str(username)):
            raise serializers.ValidationError(detail={"username":"아이디는 숫자 6자 이상 20자 이하의 영문 대/소문자 이어야 합니다."})
        
        #비밀번호 일치
        if password != repassword:
            raise serializers.ValidationError(detail={"password":"비밀번호가 일치하지 않습니다."})
        
        #비밀번호 유효성 검사
        if not re.search(PASSWORD_VALIDATION, str(password)):
            raise serializers.ValidationError(detail={"password":"비밀번호는 8자 이상 16자이하의 영문 대/소문자, 숫자, 특수문자 조합이어야 합니다. "})
        
        #비밀번호 동일여부 검사
        if re.search(PASSWORD_PATTERN, str(password)):
            raise serializers.ValidationError(detail={"password":"비밀번호는 3자리 이상 동일한 영문,숫자,특수문자 사용 불가합니다. "})
        
        #휴대폰 번호 존재여부와 blank 허용
        if User.objects.filter(phone_number=phone_number).exists() and not phone_number=='':
            raise serializers.ValidationError(detail={"phone_number":"이미 사용중인 휴대폰 번호 이거나 탈퇴한 휴대폰 번호입니다."})
        
        #이용약관 확인 검사
        if term_check == False:
            raise serializers.ValidationError(detail={"term_check":"약관동의를 확인해주세요."})
        
        return data
    
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        phone_number = validated_data['phone_number']
        
        user= User(
            username=username,
            phone_number=phone_number,
            email=email, 
        )
        user.set_password(validated_data['password'])
        user.save()
        
        Profile.objects.create(user=user)
        return user

#프로필 serializer
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('nickname', 'profile_image', 'intro', )