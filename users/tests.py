from django.urls import reverse
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, ConfirmPhoneNumber, Profile

class UserSignupAPIViewTestCase(APITestCase):
    
    #회원가입 성공
    def test_signup_success(self):
        url = reverse("user_view")
        user_data = {
            "email":"test@test.com",
            "username":"test1234",
            "phone_number":"01012341234",
            "password":"Test1234!",
            "repassword":"Test1234!",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)
    
    #회원가입 실패(이메일 빈칸)
    def test_signup_email_blank_fail(self):
        url = reverse("user_view")
        user_data = {
            "email":"",
            "username":"test1234",
            "phone_number":"01012341234",
            "password":"Test1234!",
            "repassword":"Test1234!",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
        
    #회원가입 실패(이메일 형식)
    def test_signup_email_invalid_fail(self):
        url = reverse("user_view")
        user_data = {
            "email":"test",
            "username":"test1234",
            "phone_number":"01012341234",
            "password":"Test1234!",
            "repassword":"Test1234!",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
        
    #회원가입 실패(이메일 중복)
    def test_signup_email_unique_fail(self):
        User.objects.create_user("test1234","test@test.com", "010123434321","Test1234!")
        url = reverse("user_view")
        user_data = {
            "email":"test@test.com",
            "username":"test123",
            "phone_number":"01012341234",
            "password":"Test1234!",
            "repassword":"Test1234!",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
        
    #회원가입 실패(아이디 빈칸)
    def test_signup_username_blank_fail(self):
        url = reverse("user_view")
        user_data = {
            "email":"test@test.com",
            "username":"",
            "phone_number":"01012341234",
            "password":"Test1234!",
            "repassword":"Test1234!",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
        
    #회원가입 실패(아이디 유효성검사)
    def test_signup_username_validation_fail(self):
        url = reverse("user_view")
        user_data = {
            "email":"test@test.com",
            "username":"n!!!!!!!!!",
            "phone_number":"01012341234",
            "password":"Test1234!",
            "repassword":"Test1234!",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
    
    #회원가입 실패(아이디 중복)
    def test_signup_username_unique_fail(self):
        User.objects.create_user("test1234","test@test.com", "010123434321","Test1234!")
        url = reverse("user_view")
        user_data = {
            "email":"test1@test.com",
            "username":"test1234",
            "phone_number":"01012341234",
            "password":"Test1234!",
            "repassword":"Test1234!",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
    
    #회원가입 실패(비밀번호 빈칸)
    def test_signup_password_blank_fail(self):
        url = reverse("user_view")
        user_data = {
            "email":"test@test.com",
            "username":"test1234",
            "phone_number":"01012341234",
            "password":"",
            "repassword":"Test1234!",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
    
        #회원가입 실패(아이디 중복)
    def test_signup_phone_number_unique_fail(self):
        User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        url = reverse("user_view")
        user_data = {
            "email":"test1@test.com",
            "username":"test12345",
            "phone_number":"01012341234",
            "password":"Test1234!",
            "repassword":"Test1234!",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
    
    #회원가입 실패(비밀번호확인 빈칸)
    def test_signup_password_confirm_blank_fail(self):
        url = reverse("user_view")
        user_data = {
            "email":"test@test.com",
            "username":"test1234",
            "phone_number":"01012341234",
            "password":"Test1234!",
            "repassword":"",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
        
    #회원가입 실패(비밀번호, 비밀번호 확인 일치 )
    def test_signup_password_same_fail(self):
        url = reverse("user_view")
        user_data = {
            "email":"test@test.com",
            "username":"test1234",
            "phone_number":"01012341234",            
            "password":"Test1234!",
            "repassword":"Test12345!",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
        
    #회원가입 실패(비밀번호 유효성 검사(simple))
    def test_signup_password_validation_fail(self):
        url = reverse("user_view")
        user_data = {
            "email":"test@test.com",
            "username":"test1234",
            "phone_number":"01012341234",
            "password":"t1",
            "repassword":"t1",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
        
    #회원가입 실패(비밀번호 유효성검사(동일))
    def test_signup_password_validation_same_fail(self):
        url = reverse("user_view")
        user_data = {
            "email":"test@test.com",
            "username":"test1234",
            "phone_number":"01012341234",
            "password":"Test111!",
            "repassword":"Test111!",
            "term_check":"True",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
        
    #회원가입 실패(약관동의)
    def test_signup_term_checkt_fail(self):
        url = reverse("user_view")
        user_data = {
            "email":"test@test.com",
            "username":"test1234",
            "phone_number":"01012341234",
            "password":"Test1234!",
            "repassword":"Test1234!",
            "term_check":"False",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)

class UserDeleteAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {"username": "test1234", "password":"Test1234!"}
        self.user1 = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        self.user2 = User.objects.create_user("test12345","test1@test.com", "01012351234","Test1234!")
    
    #회원 비활성화 
    def test_user_delete_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.delete(
            path=reverse("user_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)
class UserLoginLogoutAPIViewTestCase(APITestCase):
    def setUp(self):
        self.success_data = {"username": "test1234", "password":"Test1234!"}
        self.fail_data = {"username": "test12345", "password":"Test1234!!"}
        self.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        
    #(access token)로그인 성공
    def test_access_token_login_success(self):
        response = self.client.post(reverse('token_obtain_pair_view'), self.success_data)
        self.assertEqual(response.status_code, 200)
    
    #(access token)로그인 실패
    def test_access_token_login_fail(self):
        response = self.client.post(reverse('token_obtain_pair_view'), self.fail_data)
        self.assertEqual(response.status_code, 401)
        
    #(refresh_token)로그인 성공
    def test_refresh_token_login_success(self):
        token = self.client.post(reverse('token_obtain_pair_view'), self.success_data)
        access_token = token.data['access']
        refresh_token = token.data['refresh']
        response = self.client.post(
            path=reverse("token_refresh_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"refresh":refresh_token}
        )
        self.assertEqual(response.status_code, 200)
        
    #(refresh_token)로그인 실패(refresh 입력안했을 때)
    def test_refresh_token_login_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.success_data).data['access']
        response = self.client.post(
            path=reverse("token_refresh_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 400)

    #(refresh_token)로그인 실패(access 토큰 넣었을 때)
    def test_refresh_token_login_invalid_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.success_data).data['access']
        response = self.client.post(
            path=reverse("token_refresh_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"refresh":access_token}
        )
        self.assertEqual(response.status_code, 401)

    #(refresh_token)로그아웃 성공
    def test_refresh_token_logout_success(self):
        token = self.client.post(reverse('token_obtain_pair_view'), self.success_data)
        access_token = token.data['access']
        refresh_token = token.data['refresh']
        response = self.client.post(
            path=reverse("logout_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"refresh":refresh_token}
        )
        self.assertEqual(response.status_code, 200)
    
    #(refresh_token)로그아웃 실패(refresh 입력안했을 때)
    def test_refresh_token_logout_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.success_data).data['access']
        response = self.client.post(
            path=reverse("logout_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 400)
        
    #(refresh_token)로그아웃 실패(access 토큰 넣었을 때)
    def test_refresh_token_logout_invalid_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.success_data).data['access']
        response = self.client.post(
            path=reverse("logout_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"refresh":access_token}
        )
        self.assertEqual(response.status_code, 400)

class UserConfirmEmailAPIViewTest(APITestCase):
    def setUp(self):
        User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        self.user = User.objects.get(email="test@test.com")
        self.secured_key_data = RefreshToken.for_user(self.user).access_token
    
    def test_confirm_email_success(self):
        response = self.client.get(
            path=f'{reverse("confirm_email_view")}?secured_key={self.secured_key_data}',
        )
        self.assertEqual(response.status_code, 200)
        
    def test_confirm_email_fail(self):
        response = self.client.get(
            path=f'{reverse("confirm_email_view")}?secured_key={self.secured_key_data}1',
        )
        self.assertEqual(response.status_code, 400)

# class UserConfirmPhoneNumberAPIViewTest(APITestCase):
'''
휴대폰 인증번호가 진짜 발송됨으로 주의하기
'''
#     def setUp(self):
#         User.objects.create_user("test1234","test@test.com", "00000000000","Test1234!")
#         self.user = User.objects.get(email="test@test.com")
#         self.confirm_phone_number_data = ConfirmPhoneNumber.objects.create(user=self.user)
        
        
#     def test_confirm_phone_number_success(self):
#         response = self.client.post(
#             path=reverse("confirm_phone_number_view"),
#             data={"phone_number":self.user.phone_number,
#                 "auth_number":self.confirm_phone_number_data.auth_number}
#         )
#         self.assertEqual(response.status_code, 200)
        
#     def test_confirm_phone_number_auth_number_invalid_fail(self):
#         response = self.client.post(
#             path=reverse("confirm_phone_number_view"),
#             data={"phone_number":self.user.phone_number,
#                 "auth_number":1234}
#         )
#         print(response.data)
#         self.assertEqual(response.status_code, 400)

class ProfileUpdateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {"username": "test12341", "password":"Test1234!"}
        self.user1 = User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")
        self.user2 = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        
        self.profile1 = Profile.objects.create(user=self.user1, nickname="test", intro='test')
        self.profile2 = Profile.objects.create(user=self.user2, nickname="test1", intro='test1')
    
    #회원정보 수정 성공
    def test_profile_update_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("private_profile_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"nickname":"test111", "intro":"testtest"} 
        )
        self.assertEqual(response.status_code, 200)
        
    #회원정보 수정 실패(닉네임 유효성검사)
    def test_profile_update_nickname_validation_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("private_profile_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"nickname":"d!",  "intro":"testtest"} 
        )
        self.assertEqual(response.status_code, 400)
    
    #회원정보 수정 실패(닉네임 중복)
    def test_profile_update_nickname_unique_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("private_profile_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"nickname":"test1", "intro":"testtest"} 
        )
        self.assertEqual(response.status_code, 400)

class ChangePasswordAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {"username": "test12341", "password":"Test1234!"}
        self.user = User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")

    #비밀번호 변경 인증 성공
    def test_password_change_confirm_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.post(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!"} 
        )
        self.assertEqual(response.status_code, 200)
    
    #비밀번호 변경 인증 실패
    def test_password_change_confirm_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.post(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test!"} 
        )
        self.assertEqual(response.status_code, 400)
    
    #비밀번호 변경 성공
    def test_password_change_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":"Test1234!!"} 
        )
        self.assertEqual(response.status_code, 200)
    
    #비밀번호 변경 실패(비밀번호 빈칸)
    def test_password_change_password_blank_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"", "repassword":"Test1234!!"} 
        )
        self.assertEqual(response.status_code, 400)

    #비밀번호 변경 실패(비밀번호 확인 빈칸)
    def test_password_change_password_confirm_blank_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":""} 
        )
        self.assertEqual(response.status_code, 400)
        
    #비밀번호 변경 실패(비밀번호 현재비밀번호와 동일시)
    def test_password_change_current_password_same_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!", "repassword":"Test1234!"} 
        )
        
        self.assertEqual(response.status_code, 400)
        
    #비밀번호 변경 실패(비밀번호 유효성검사(simple))
    def test_password_change_password_validation_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234", "repassword":"Test1234"} 
        )
        self.assertEqual(response.status_code, 400)
        
    #비밀번호 변경 실패(비밀번호 유효성검사(동일))
    def test_password_change_password_validation_same_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test111!", "repassword":"Test111!"} 
        )
        self.assertEqual(response.status_code, 400)
    
    #비밀번호 변경 실패(비밀번호, 비밀번호 확인 일치 )
    def test_password_change_password_same_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":"Test1234!"} 
        )
        self.assertEqual(response.status_code, 400)

class PasswordTokenCheckAPIViewTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")
        
        self.user = User.objects.get(email="test1@test.com")
        self.uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id)) 
        self.token = PasswordResetTokenGenerator().make_token(self.user)
        

    #비밀번호 토큰 인증 성공
    def test_password_token_check_success(self):
        response = self.client.get(
            path=reverse("password_reset_confirm_view", kwargs={'uidb64':self.uidb64, 'token':self.token}),
        )
        self.assertEqual(response.status_code, 200)

    def test_password_token_check_fail(self):
        response = self.client.get(
            path=reverse("password_reset_confirm_view", kwargs={'uidb64':"11", 'token':"11"})
        )
        self.assertEqual(response.status_code, 401)

class SetPasswordAPIViewTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")
        
        self.user = User.objects.get(email="test1@test.com")
        self.uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id)) 
        self.token = PasswordResetTokenGenerator().make_token(self.user)
        
    #비밀번호 변경 성공
    def test_password_set_success(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"Test1234!!", "repassword":"Test1234!!", "uidb64":self.uidb64, "token": self.token} 
        )
        self.assertEqual(response.status_code, 200)
    
    #비밀번호 변경 실패(비밀번호 빈칸)
    def test_password_selt_password_blank_fail(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"", "repassword":"Test1234!!", "uidb64":self.uidb64, "token": self.token} 
        )
        self.assertEqual(response.status_code, 400)

    #비밀번호 변경 실패(비밀번호 확인 빈칸)
    def test_password_set_password_confirm_blank_fail(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"Test1234!!", "repassword":"", "uidb64":self.uidb64, "token": self.token} 
        )
        self.assertEqual(response.status_code, 400)
        
    #비밀번호 변경 실패(비밀번호 유효성검사(simple))
    def test_password_set_password_validation_fail(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"Test1234", "repassword":"Test1234", "uidb64":self.uidb64, "token": self.token} 
        )
        self.assertEqual(response.status_code, 400)
        
    #비밀번호 변경 실패(비밀번호 유효성검사(동일))
    def test_password_set_password_validation_same_fail(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"Test111!", "repassword":"Test111!",  "uidb64":self.uidb64, "token": self.token} 
        )
        self.assertEqual(response.status_code, 400)
    
    #비밀번호 변경 실패(비밀번호, 비밀번호 확인 일치 )
    def test_password_set_password_same_fail(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"Test1234!!", "repassword":"Test1234!", "uidb64":self.uidb64, "token": self.token} 
        )
        self.assertEqual(response.status_code, 400)
    
    def test_password_set_password_token_fail(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"Test1234!!", "repassword":"Test1234!!", "uidb64":self.uidb64, "token": "1234"} 
        )
        self.assertEqual(response.status_code, 401)
