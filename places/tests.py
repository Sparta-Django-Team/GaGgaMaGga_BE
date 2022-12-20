from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User, Profile
from places.models import Place



#### 장소 ####
class ReviewRankAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username':'test1234', 'password':'Test1234!'}
        cls.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        Profile.objects.create(user=cls.user)
        cls.place = Place.objects.create(place_name="장소명", category="카테고리", rating="5", place_address="주소", place_time="시간", place_img="이미지")

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair_view'), self.user_data).data['access']
    
    # 장소 추천 카테고리 선택
    def test_place_selection_(self):
        response = self.client.get(
            path=reverse("place_select_view"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.assertEqual(response.status_code, 200)
