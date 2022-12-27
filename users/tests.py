from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY

from PIL import Image
import tempfile

from .models import User, ConfirmPhoneNumber, Profile, BlockedCountryIP


def get_temporary_image(temp_file):
    size = (200,200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file


class UserSignupAPIViewTestCase(APITestCase):
    
    # 회원가입 성공
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
    
    # 회원가입 실패(이메일 빈칸)
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
        
    # 회원가입 실패(이메일 형식)
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
        
    # 회원가입 실패(이메일 중복)
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
        
    # 회원가입 실패(아이디 빈칸)
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
        
    # 회원가입 실패(아이디 유효성검사)
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
    
    # 회원가입 실패(아이디 중복)
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
    
    # 회원가입 실패(비밀번호 빈칸)
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
    
    # 회원가입 실패(전화번호 중복)
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
    
    # 회원가입 실패(비밀번호확인 빈칸)
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
        
    # 회원가입 실패(비밀번호, 비밀번호 확인 일치 )
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
        
    # 회원가입 실패(비밀번호 유효성 검사(simple))
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
        
    # 회원가입 실패(비밀번호 유효성검사(동일))
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
        
    # 회원가입 실패(약관동의)
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


class UserUpdateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {"username": "test1234", "password":"Test1234!"}
        self.user1 = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        self.user2 = User.objects.create_user("test12345","test1@test.com", "01012351234","Test1234!")
        Profile.objects.create(user=self.user1)
        Profile.objects.create(user=self.user2)
    
    # 회원정보 수정 성공
    def test_user_update_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("user_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"email":"test2@test.com", "phone_number":"01098765432"}
        )
        self.assertEqual(response.status_code, 200)
        
    # 회원정보 수정 실패(이메일 빈칸)
    def test_user_update_email_blank_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("user_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"email":"","phone_number":"01098765432"}
        )
        self.assertEqual(response.status_code, 400)
        
    # 회원정보 수정 실패(이메일 중복)
    def test_user_update_email_unique_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("user_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"email":"test1@test.com","phone_number":"01098765432"}
        )
        self.assertEqual(response.status_code, 400)
        
    # 회원정보 수정 실패(이메일 형식)
    def test_user_update_email_invalid_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("user_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"email":"test1","phone_number":"01098765432"}
        )
        self.assertEqual(response.status_code, 400)
        
    # 회원정보 수정 실패(휴대폰번호 중복)
    def test_user_update_phone_number_unique_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("user_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"email":"test2@test.com","phone_number":"01012351234"}
        )
        self.assertEqual(response.status_code, 400)


class UserDeleteAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {"username": "test1234", "password":"Test1234!"}
        self.user1 = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        self.user2 = User.objects.create_user("test12345","test1@test.com", "01012351234","Test1234!")
        Profile.objects.create(user=self.user1)
        Profile.objects.create(user=self.user2)

    # 회원 비활성화 
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
        self.fail_data = {"username": "test1234", "password":"Test1234!!"}
        self.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        Profile.objects.create(user=self.user)
        
    # (access_token)로그인 성공
    def test_access_token_login_success(self):
        response = self.client.post(reverse('token_obtain_pair_view'), self.success_data)
        self.assertEqual(response.status_code, 200)
    
    # (access_token)로그인 실패
    def test_access_token_login_fail(self):
        response = self.client.post(reverse('token_obtain_pair_view'), self.fail_data)
        self.assertEqual(response.status_code, 401)
        
    # (accss_token 여러번 시도)로그인 실패
    def test_access_token_login_attempt_fail(self):
        self.client.post(reverse('token_obtain_pair_view'), self.fail_data)
        self.client.post(reverse('token_obtain_pair_view'), self.fail_data)
        self.client.post(reverse('token_obtain_pair_view'), self.fail_data)
        self.client.post(reverse('token_obtain_pair_view'), self.fail_data)
        self.client.post(reverse('token_obtain_pair_view'), self.fail_data)
        response = self.client.post(reverse('token_obtain_pair_view'), self.success_data)
        self.assertEqual(response.status_code, 400)
        
    # (refresh_token)로그인 성공
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
        
    # (refresh_token)로그인 실패(refresh 입력안했을 때)
    def test_refresh_token_login_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.success_data).data['access']
        response = self.client.post(
            path=reverse("token_refresh_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 400)

    # (refresh_token)로그인 실패(access 토큰 넣었을 때)
    def test_refresh_token_login_invalid_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.success_data).data['access']
        response = self.client.post(
            path=reverse("token_refresh_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"refresh":access_token}
        )
        self.assertEqual(response.status_code, 401)

    # (refresh_token)로그아웃 성공
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
    
    # (refresh_token)로그아웃 실패(refresh 입력안했을 때)
    def test_refresh_token_logout_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.success_data).data['access']
        response = self.client.post(
            path=reverse("logout_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 400)
        
    # (refresh_token)로그아웃 실패(access 토큰 넣었을 때)
    def test_refresh_token_logout_invalid_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.success_data).data['access']
        response = self.client.post(
            path=reverse("logout_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"refresh":access_token}
        )
        self.assertEqual(response.status_code, 400)
    
    # access_token 유효한지
    def test_access_token_verify_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.success_data).data['access']
        response = self.client.post(
            path=reverse("token_verify"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"token":access_token}
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)
        
    # refresh_token 유효
    def test_refresh_token_verify_success(self):
        token = self.client.post(reverse('token_obtain_pair_view'), self.success_data)
        access_token = token.data['access']
        refresh_token = token.data['refresh']
        response = self.client.post(
            path=reverse("token_verify"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"token":refresh_token}
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)
        
    # token 유효하지 않음
    def test_token_verify_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.success_data).data['access']
        response = self.client.post(
            path=reverse("token_verify"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"token": f"{access_token}123"}
        )
        print(response.data)
        self.assertEqual(response.status_code, 401)
    
        
    # 일괄 로그아웃 성공
    def test_bulk_logout_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.success_data).data['access']
        response = self.client.post(
            path=reverse("bulk_logout_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)


class UserConfirmEmailAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        self.secured_key_data = RefreshToken.for_user(self.user).access_token
    
    # 이메일 인증 성공
    def test_confirm_email_success(self):
        response = self.client.get(
            path=f'{reverse("confirm_email_view")}?secured_key={self.secured_key_data}',
        )
        self.assertEqual(response.status_code, 200)
    
    # 이메일 인증 실패
    def test_confirm_email_fail(self):
        response = self.client.get(
            path=f'{reverse("confirm_email_view")}?secured_key={self.secured_key_data}1',
        )
        self.assertEqual(response.status_code, 400)

class UserResendEmailAPIViewTest(APITestCase):
    def setUp(self):
        self.data = {"username": "test1234", "password":"Test1234!"}
        self.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        Profile.objects.create(user=self.user)
    
    # 이메일 재전송 성공
    def test_resend_email_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.post(
            path=reverse("resend_email_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)

    # 이메일 재전송 실패
    def test_resend_email_fail(self):
        response = self.client.post(
            path=reverse("resend_email_view"),
        )
        self.assertEqual(response.status_code, 401)


class SendPhoneNumberAPIViewTest(APITestCase):
    def setUp(self):
        User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
    
    # 아이디 찾기 인증번호 보내기 성공
    def test_send_phone_number_success(self):
        response = self.client.post(
            path=reverse("send_phone_number_view"),
            data={"phone_number":"01012341234"}
        )
        self.assertEqual(response.status_code, 200)

    # 아이디 찾기 인증번호 보내기 실패
    def test_send_phone_number_fail(self):
        response = self.client.post(
            path=reverse("send_phone_number_view"),
            data={"phone_number":"01012341235"}
        )
        self.assertEqual(response.status_code, 400)


class UserConfirmPhoneNumberAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test1234","test@test.com", "00000000000","Test1234!")
        self.confirm_phone_number_data = ConfirmPhoneNumber.objects.create(user=self.user)
    
    # 아이디 찾기 인증번호 확인 성공
    def test_confirm_phone_number_success(self):
        response = self.client.post(
            path=reverse("confirm_phone_number_view"),
            data={"phone_number":self.user.phone_number,
                "auth_number":self.confirm_phone_number_data.auth_number}
        )
        self.assertEqual(response.status_code, 200)
    
    # 아이디 찾기 인증번호 확인 실패
    def test_confirm_phone_number_auth_number_invalid_fail(self):
        response = self.client.post(
            path=reverse("confirm_phone_number_view"),
            data={"phone_number":self.user.phone_number,
                "auth_number":1234}
        )
        self.assertEqual(response.status_code, 400)


class PrivateProfileAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {"username": "test12341", "password":"Test1234!"}
        self.user1 = User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")
        self.user2 = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        self.profile1 = Profile.objects.create(user=self.user1, nickname="test", intro='test')
        self.profile2 = Profile.objects.create(user=self.user2, nickname="test1", intro='test1')
    
    # 개인 프로필
    def test_private_profile_get_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.get(
            path=reverse("private_profile_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)

    # 프로필 수정 성공
    def test_profile_update_success(self):
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)
        
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("private_profile_view"),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data=encode_multipart(data={"nickname":"test111", "intro":"testtest", "profile_image":image_file}, boundary=BOUNDARY) 
        )
        self.assertEqual(response.status_code, 200)
        
    # 프로필 수정 실패(닉네임 유효성검사)
    def test_profile_update_nickname_validation_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("private_profile_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"nickname":"d!",  "intro":"testtest"} 
        )
        self.assertEqual(response.status_code, 400)
    
    # 프로필 수정 실패(닉네임 중복)
    def test_profile_update_nickname_unique_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("private_profile_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"nickname":"test1", "intro":"testtest"} 
        )
        self.assertEqual(response.status_code, 400)


class PublicProfileAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {"username": "test1234", "password":"Test1234!"}
        self.user1 = User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")
        self.user2 = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        
        self.profile1 = Profile.objects.create(user=self.user1, nickname="test1", intro='test')
        self.profile2 = Profile.objects.create(user=self.user2, nickname="test2", intro='test')
    
    # 공개 프로필
    def test_public_profile_get_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.get(
            path=reverse("public_profile_view", kwargs={"nickname":"test1"}),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)


class CountyIPBlockAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {"username": "test1234", "password":"Test1234!"}
        self.user = User.objects.create_user("test1234","test1@test.com", "01012351234","Test1234!")
        Profile.objects.create(user=self.user)
        BlockedCountryIP.objects.create(country="KR", user=self.user)
        

    # IP 국가코드 차단 읽기 성공
    def test_country_ip_block_get_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.get(
            path=reverse("country_ip_block_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)
    
    # IP 국가코드 차단 성공
    def test_country_ip_block_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.post(
            path=reverse("country_ip_block_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"country":"CN"}
        )
        self.assertEqual(response.status_code, 201)
    
    # IP 국가코드 차단 실패 (국가코드 중복)
    def test_country_ip_block_unique_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.post(
            path=reverse("country_ip_block_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"country":"KR"}
        )
        self.assertEqual(response.status_code, 400)

    # IP 국가코드 차단 실패 (국가코드 빈칸)
    def test_country_ip_block_blank_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.post(
            path=reverse("country_ip_block_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"country":""}
        )
        self.assertEqual(response.status_code, 400)
        
    # IP 국가코드 차단 삭제 
    def test_country_ip_block_delete_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.delete(
            path=reverse("country_ip_block_delete_view", kwargs={'country_id':"1"}),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)


class LoginLogListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {"username": "test1234", "password":"Test1234!"}
        self.user = User.objects.create_user("test1234","test1@test.com", "01012351234","Test1234!")
        Profile.objects.create(user=self.user)

    # 로그인 기록
    def test_login_log_get_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.get(
            path=reverse("login_log_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)

class ChangePasswordAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {"username": "test12341", "password":"Test1234!"}
        self.user = User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")
        Profile.objects.create(user=self.user)

    # 비밀번호 변경 성공
    def test_password_change_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":"Test1234!!", "confirm_password":"Test1234!"} 
        )
        self.assertEqual(response.status_code, 200)
    
    # 현재 비밀번호 확인(비밀번호 빈칸)
    def test_password_change_confirm_password_blank_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":"Test1234!!", "confirm_password":""} 
        )
        self.assertEqual(response.status_code, 400)
        
    # 현재 비밀번호 확인(비밀번호 불일치)
    def test_password_change_confirm_password_invaild_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":"Test1234!!", "confirm_password":"Test1234"} 
        )
        self.assertEqual(response.status_code, 400)
    
    # 비밀번호 변경 실패(비밀번호 빈칸)
    def test_password_change_password_blank_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"", "repassword":"Test1234!!", "confirm_password":"Test1234!"} 
        )
        self.assertEqual(response.status_code, 400)

    # 비밀번호 변경 실패(비밀번호 확인 빈칸)
    def test_password_change_password_confirm_blank_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":"", "confirm_password":"Test1234!"} 
        )
        self.assertEqual(response.status_code, 400)
        
    # 비밀번호 변경 실패(비밀번호 현재 비밀번호와 동일시)
    def test_password_change_current_password_same_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!", "repassword":"Test1234!", "confirm_password":"Test1234!"} 
        )
        
        self.assertEqual(response.status_code, 400)
        
    # 비밀번호 변경 실패(비밀번호 유효성검사(simple))
    def test_password_change_password_validation_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234", "repassword":"Test1234", "confirm_password":"Test1234!"} 
        )
        self.assertEqual(response.status_code, 400)
        
    # 비밀번호 변경 실패(비밀번호 유효성검사(동일))
    def test_password_change_password_validation_same_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test111!", "repassword":"Test111!", "confirm_password":"Test1234!"} 
        )
        self.assertEqual(response.status_code, 400)
    
    # 비밀번호 변경 실패(비밀번호, 비밀번호 확인 일치 )
    def test_password_change_password_same_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":"Test1234!", "confirm_password":"Test1234!"} 
        )
        self.assertEqual(response.status_code, 400)


class PasswordResetAPIViewTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")
    
    # 비밀번호 찾기 이메일 전송 성공
    def test_password_reset_email_success(self):
        response = self.client.post(
            path=reverse("password_reset_email_view"),
            data={"email":"test1@test.com"} 
        )
        self.assertEqual(response.status_code, 200)
    
    # 존재하지 않는 이메일전송
    def test_password_reset_email_fail(self):
        response = self.client.post(
            path=reverse("password_reset_email_view"),
            data={"email":"test2@test.com"} 
        )
        self.assertEqual(response.status_code, 400)
        
    # 형식에 맞지 않는 이메일전송
    def test_password_reset_email_invalid_fail(self):
        response = self.client.post(
            path=reverse("password_reset_email_view"),
            data={"email":"test2"} 
        )
        self.assertEqual(response.status_code, 400)
        
    # 이메일 빈칸일 때 이메일 전송
    def test_password_reset_email_blank_fail(self):
        response = self.client.post(
            path=reverse("password_reset_email_view"),
            data={"email":""} 
        )
        self.assertEqual(response.status_code, 400)


class PasswordTokenCheckAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")
        self.uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id)) 
        self.token = PasswordResetTokenGenerator().make_token(self.user)

    # 비밀번호 토큰 인증 성공
    def test_password_token_check_success(self):
        response = self.client.get(
            path=reverse("password_reset_confirm_view", kwargs={'uidb64':self.uidb64, 'token':self.token}),
        )
        self.assertEqual(response.status_code, 200)

    # 비밀번호 토큰 인증 실패
    def test_password_token_check_fail(self):
        response = self.client.get(
            path=reverse("password_reset_confirm_view", kwargs={'uidb64':"11", 'token':"11"})
        )
        self.assertEqual(response.status_code, 401)


class SetPasswordAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")
        self.uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id)) 
        self.token = PasswordResetTokenGenerator().make_token(self.user)
        
    # 비밀번호 재설정 성공
    def test_password_set_success(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"Test1234!!", "repassword":"Test1234!!", "uidb64":self.uidb64, "token": self.token} 
        )
        self.assertEqual(response.status_code, 200)
    
    # 비밀번호 재설정 실패(비밀번호 빈칸)
    def test_password_set_password_blank_fail(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"", "repassword":"Test1234!!", "uidb64":self.uidb64, "token": self.token} 
        )
        self.assertEqual(response.status_code, 400)

    # 비밀번호 재설정 실패(비밀번호 확인 빈칸)
    def test_password_set_password_confirm_blank_fail(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"Test1234!!", "repassword":"", "uidb64":self.uidb64, "token": self.token} 
        )
        self.assertEqual(response.status_code, 400)
        
    # 비밀번호 재설정 실패(비밀번호 유효성검사(simple))
    def test_password_set_password_validation_fail(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"Test1234", "repassword":"Test1234", "uidb64":self.uidb64, "token": self.token} 
        )
        self.assertEqual(response.status_code, 400)
        
    # 비밀번호 재설정 실패(비밀번호 유효성검사(동일))
    def test_password_set_password_validation_same_fail(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"Test111!", "repassword":"Test111!",  "uidb64":self.uidb64, "token": self.token} 
        )
        self.assertEqual(response.status_code, 400)
    
    # 비밀번호 재설정 실패(비밀번호, 비밀번호 확인 일치 )
    def test_password_set_password_same_fail(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"Test1234!!", "repassword":"Test1234!", "uidb64":self.uidb64, "token": self.token} 
        )
        self.assertEqual(response.status_code, 400)
    
    # 토큰이 다를 경우
    def test_password_set_password_token_fail(self):
        response = self.client.put(
            path=reverse("password_reset_complete_view"),
            data={"password":"Test1234!!", "repassword":"Test1234!!", "uidb64":self.uidb64, "token": "1234"} 
        )
        self.assertEqual(response.status_code, 401)


class ExpiredPasswordChageAPIView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")
        Profile.objects.create(user=self.user, nickname="test", intro='test')
        
        self.user.password_expired = True
        self.user.save()
        
        self.data = {"username": "test12341", "password":"Test1234!"}
    
    # 비밀번호 만료 확인 성공
    def test_expired_password_get_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.get(
            path=reverse("password_expired_change_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)
    
    # 비밀번호 다음에 변경하기 성공
    def test_expired_password_post_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.post(
            path=reverse("password_expired_change_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)
        
    # 비밀번호 변경 성공
    def test_expired_password_put_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("password_expired_change_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":"Test1234!!", "confirm_password":"Test1234!"} 
        )
        self.assertEqual(response.status_code, 200)
        
    # 현재 비밀번호 확인 실패(비밀번호 빈칸)
    def test_expired_password_confirm_password_blank_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":"Test1234!!", "confirm_password":""} 
        )
        self.assertEqual(response.status_code, 400)
        
    # 현재 비밀번호 확인 실패(비밀번호 불일치)
    def test_expired_password_confirm_password_invaild_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("change_password_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":"Test1234!!", "confirm_password":"Test1234"} 
        )
        self.assertEqual(response.status_code, 400)
    
    # 비밀번호 변경 실패(비밀번호 빈칸)
    def test_expired_password_put_blank_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("password_expired_change_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"", "repassword":"Test1234!!", "confirm_password":"Test1234"} 
        )
        self.assertEqual(response.status_code, 400)

    # 비밀번호 변경 실패(비밀번호 확인 빈칸)
    def test_expired_password_put_confirm_blank_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("password_expired_change_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":"", "confirm_password":"Test1234"} 
        )
        self.assertEqual(response.status_code, 400)
        
    # 비밀번호 변경 실패(비밀번호 유효성검사(simple))
    def test_expired_password_put_validation_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("password_expired_change_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234", "repassword":"Test1234", "confirm_password":"Test1234"} 
        )
        self.assertEqual(response.status_code, 400)
        
    # 비밀번호 변경 실패(비밀번호 유효성검사(동일))
    def test_expired_password_put_validation_same_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("password_expired_change_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test111!", "repassword":"Test111!", "confirm_password":"Test1234"} 
        )
        self.assertEqual(response.status_code, 400)
    
    # 비밀번호 변경 실패(비밀번호, 비밀번호 확인 일치 )
    def test_expired_password_put_same_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.data).data['access']
        response = self.client.put(
            path=reverse("password_expired_change_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            data={"password":"Test1234!!", "repassword":"Test1234!", "confirm_password":"Test1234"} 
        )
        self.assertEqual(response.status_code, 400)


class FollowAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")
        self.user2 = User.objects.create_user("test12342","test2@test.com", "01012351235","Test1234!")

        self.profile1 = Profile.objects.create(user=self.user1, nickname="test", intro='test')
        self.profile2 = Profile.objects.create(user=self.user2, nickname="test1", intro="test")
        
        self.user = {"username": "test12341", "password":"Test1234!"}
    
    # 팔로우 성공
    def test_follow_success(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.user).data['access']
        response_case_1 = self.client.post(
            path=reverse("process_follow_view", kwargs={"nickname":"test1"}),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        
        self.assertEqual(response_case_1.status_code, 200)
        
        response_case_2 = self.client.post(
            path=reverse("process_follow_view", kwargs={"nickname":"test1"}),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response_case_2.status_code, 200)
        
    def test_follow_fail(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.user).data['access']
        response = self.client.post(
            path=reverse("process_follow_view", kwargs={"nickname":"test"}),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 400)