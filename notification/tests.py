from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import User, Profile
from .models import Notification


# 로그인한 사용자가 읽지 않은 알람 불러오기
class NotificationViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username': 'test1234', 'password': 'Test1234!'}
        cls.user = User.objects.create_user("test1234", "test@test.com", "01012341234", "Test1234!")
        Profile.objects.create(user=cls.user, nickname="user", intro="test")
        cls.Notification = Notification.objects.create(user=cls.user, content="게시글에 덧글이 달렸습니다.", is_seen=0)

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair_view'), self.user_data).data['access']

    # 전체 리뷰 조회 성공
    def test_notification_list_success(self):
        profile_response = self.client.get(
            path=reverse("private_profile_view"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
            )

        response = self.client.get(
            path=reverse("notification", kwargs={'user_id': profile_response.data["id"]}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
            )
        self.assertEqual(response.status_code, 200)

class NotificationDetailView(APITestCase):
    def setUp(self):
        self.user_data = {"username": "test12341", "password": "Test1234!"}
        self.user = User.objects.create_user("test12341", "test1@test.com", "01012351234", "Test1234!")
        self.profile = Profile.objects.create(user=self.user, nickname="test", intro='test')
        self.notification = Notification.objects.create(user=self.user, content="게시글에 덧글이 달렸습니다.", is_seen=0)

    def test_see_nofication(self):
        access_token = self.client.post(reverse('token_obtain_pair_view'), self.user_data).data['access']
        response = self.client.put(
            path=reverse("notification_detail", kwargs={"notification_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)