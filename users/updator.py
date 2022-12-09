import sys
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaggamagga.settings')
django.setup()

from django.utils import timezone

from users.models import User
from users.utils import Util

class UserStatusChange:

    def __init__(self):
        self.year_ago = timezone.now() - timezone.timedelta(days=365)
        self.two_months_ago = timezone.now() - timezone.timedelta(days=60)

    # 회원정보 보유기간 지나면 withdraw True로 만듬
    def user_withdraw_send_email(self):
        user = User.objects.filter(is_admin=False, last_login__lte=self.year_ago)

        inactivate_user_email = user.values("email")
        inactivate_email_subject = '가까? 마까? 휴면회원 계정 처리 안내'
        inactivate_email_body = '고객님 안녕하세요. 가까? 마까?입니다. 저희는 소중한 고객님의 개인정보 보호를 위해 관계 법령에 따라 고객님의 온라인 계정을 별도로 분리 보관할 예정입니다. 휴면계정을 해제하기 위해서는 별도의 인증 동의 절차가 진행될 수 있으므로 편리한 계정 사용이 필요하시다면 지금 바로 가까? 마까?를 방문해주세요.'

        if user:
            for i in inactivate_user_email:
                message = {'email_body': inactivate_email_body, 'to_email': i["email"],'email_subject': inactivate_email_subject}
                Util.send_email(message)
            user.update(withdraw=True)

    # 비활성화가 되고 60일이 지나면 삭제
    def user_withdraw_delete(self):
        user = User.objects.filter(is_admin=False,  withdraw_at__lte=self.two_months_ago, withdraw=True)
        
        delete_user_email = user.values("email")
        delete_email_subject = '가까? 마까? 비활성화 계정 삭제'
        delete_email_body = '고객님 안녕하세요. 가까? 마까?입니다. 저희는 비활성화계정을 삭제합니다.'

        if user:
            for i in delete_user_email:
                message = {'email_body': delete_email_body, 'to_email': i["email"],'email_subject': delete_email_subject}
                Util.send_email(message)
            user.delete()

    # 로그인 비밀번호 변경이 60일이 지났을 경우 password_expired를 True로 바꿈
    def user_password_expired(self):
        user = User.objects.filter(is_admin=False, last_password_changed__lte=self.two_months_ago)
        user.update(password_expired=True)
