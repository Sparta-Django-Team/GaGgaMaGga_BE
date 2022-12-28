from rest_framework.test import APITestCase

from django.urls import reverse

from users.models import User, Profile
from reviews.models import Review
from .models import Place
from .views import CHOICE_CATEGORY

import random


#### 장소 ####
class PlaceSelectAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(24):
            j = round(i / 2)
            cls.place = Place.objects.create(
                place_name=f"장소{i}",
                category=CHOICE_CATEGORY[j][1],
                rating=random.randint(1, 5),
                place_address=random.choice(["제주시", "서귀포시"]),
                place_time="영업시간",
                place_img="img_url",
            )

        for i in range(30):
            cls.user = User.objects.create_user(f"user{i+1}", f"user{i+1}@test.com", "01000000000", "Test1234!")

        for i in range(100):
            cls.review = Review.objects.create(
                content="some content",
                rating_cnt=random.randint(1, 5),
                author=cls.user,
                place_id=random.randint(1, 24),
            )

    # 1. [비로그인] 카테고리 선택(place_preference.html, 음식 선택)
    def test_place_select_1(self):
        category_no1 = random.randint(1, 12)
        response = self.client.get(
            path=reverse("place_select_view", kwargs={"choice_no": category_no1})
        )
        self.assertEqual(response.status_code, 200)

    # 2. [비로그인] 카테고리 선택(place_preference.html, 장소 선택)
    def test_place_select_2(self):
        category_no2 = random.randint(13, 14)
        response = self.client.get(
            path=reverse("place_select_view", kwargs={"choice_no": category_no2})
        )
        self.assertEqual(response.status_code, 200)


# 3/4. [비로그인] 장소 리스트 불러오기(place_list.html, index에서 음식/장소 선택 > 선호도 선택)
class PlaceListNewUserAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(24):
            j = round(i / 2)
            cls.place = Place.objects.create(
                place_name=f"장소{i}",
                category=CHOICE_CATEGORY[j][1],
                rating=random.randint(1, 5),
                place_address=random.choice(["제주시", "서귀포시"]),
                place_time="영업시간",
                place_img="img_url",
            )
            
        for i in range(30):
            cls.user = User.objects.create_user(f"user{i+1}", f"user{i+1}@test.com", "01000000000", "Test1234!")
            
        for i in range(100):
            cls.review = Review.objects.create(
                content="some content",
                rating_cnt=random.randint(1, 5),
                author=cls.user,
                place_id=random.randint(1, 24),
            )

    # 음식 선택(1~12)
    def test_place_list_1(self):  # 분식
        place_id = 1
        category = CHOICE_CATEGORY[0][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_2(self):  # 한식
        place_id = 2
        category = CHOICE_CATEGORY[1][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_3(self):  # 돼지고기구이
        place_id = 3
        category = CHOICE_CATEGORY[2][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_4(self):  # 치킨,닭강정
        place_id = 4
        category = CHOICE_CATEGORY[3][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_5(self):  # 햄버거
        place_id = 5
        category = CHOICE_CATEGORY[4][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_6(self):  # 피자
        place_id = 6
        category = CHOICE_CATEGORY[5][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_7(self):  # 중식
        place_id = 7
        category = CHOICE_CATEGORY[6][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_8(self):  # 일식
        place_id = 8
        category = CHOICE_CATEGORY[7][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_9(self):  # 양식
        place_id = 9
        category = CHOICE_CATEGORY[8][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_10(self):  # 태국음식
        place_id = 10
        category = CHOICE_CATEGORY[9][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_11(self):  # 인도음식
        place_id = 11
        category = CHOICE_CATEGORY[10][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_12(self):  # 베트남음식
        place_id = 12
        category = CHOICE_CATEGORY[11][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    # 장소 선택(13~14)
    def test_place_list_13(self):  # 제주시
        place_id = 13
        category = CHOICE_CATEGORY[12][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_14(self):  # 서귀포시
        place_id = 14
        category = CHOICE_CATEGORY[13][1]
        response = self.client.get(
            path=reverse(
                "new_user_place_list_view",
                kwargs={"place_id": place_id, "category": category},
            )
        )
        self.assertEqual(response.status_code, 200)


# 5/6. [로그인] 장소 리스트 불러오기(place_list.html, index에서 음식/장소 선택)
class PlaceListUserAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(24):
            j = round(i / 2)
            cls.place = Place.objects.create(
                place_name=f"장소{i}",
                category=CHOICE_CATEGORY[j][1],
                rating=random.randint(1, 5),
                place_address=random.choice(["제주시", "서귀포시"]),
                place_time="영업시간",
                place_img="img_url",
            )

        for i in range(30):
            cls.user = User.objects.create_user(f"user{i+1}", f"user{i+1}@test.com", "01000000000", "Test1234!")
            Profile.objects.create(user=cls.user, review_cnt=1)

        for i in range(100):
            cls.review = Review.objects.create(
                content="some content",
                rating_cnt=random.randint(1, 5),
                author=cls.user,
                place_id=random.randint(1, 24),
            )

        cls.user_data = {"username": "test1234", "password": "Test1234!"}
        cls.user = User.objects.create_user("test1234", "test1@test.com", "01012341234", "Test1234!")
        Profile.objects.create(user=cls.user, review_cnt=100)

        for i in range(24):
            cls.review = Review.objects.create(
                content="some content",
                rating_cnt=random.randint(1, 5),
                author=cls.user,
                place_id=i + 1,
            )

    def setUp(self):
        self.access_token = self.client.post(reverse("token_obtain_pair_view"), self.user_data).data["access"]

    # 음식 선택(1~12)
    def test_place_list_1(self):  # 분식, 한식, 돼지고기
        cate_id = 3
        response = self.client.get(
            path=reverse("user_place_list_view", kwargs={"cate_id": cate_id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_2(self):  # 치킨,닭강정, 햄버거, 피자
        cate_id = 6
        response = self.client.get(
            path=reverse("user_place_list_view", kwargs={"cate_id": cate_id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_3(self):  # 중식
        cate_id = 7
        response = self.client.get(
            path=reverse("user_place_list_view", kwargs={"cate_id": cate_id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_4(self):  # 일식
        cate_id = 8
        response = self.client.get(
            path=reverse("user_place_list_view", kwargs={"cate_id": cate_id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_5(self):  # 양식
        cate_id = 9
        response = self.client.get(
            path=reverse("user_place_list_view", kwargs={"cate_id": cate_id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_6(self):  # 태국음식, 인도음식, 베트남음식
        cate_id = 12
        response = self.client.get(
            path=reverse("user_place_list_view", kwargs={"cate_id": cate_id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

    # 장소 선택(13~14)
    def test_place_list_7(self):  # 제주시
        cate_id = 13
        response = self.client.get(
            path=reverse("user_place_list_view", kwargs={"cate_id": cate_id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_place_list_8(self):  # 서귀포시
        cate_id = 14
        response = self.client.get(
            path=reverse("user_place_list_view", kwargs={"cate_id": cate_id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)


class PlaceDetailAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_normal_data = {"username": "test1234", "password": "Test1234!"}
        cls.user_admin_data = {"username": "admin", "password": "Test1234!"}
        cls.user_normal = User.objects.create_user("test1234", "test1@test.com", "01012341234", "Test1234!")
        cls.user_admin = User.objects.create_user("admin", "admin@test.com", "01012341235", "Test1234!")
        cls.user_admin.is_admin = True
        cls.user_admin.save()
        Profile.objects.create(user=cls.user_normal)
        Profile.objects.create(user=cls.user_admin)
        cls.place = Place.objects.create(
            place_name="장소",
            category="한식",
            rating=5,
            place_address="제주시",
            place_time="영업시간",
            place_img="img_url",
        )

    def setUp(self):
        self.access_token_normal = self.client.post(reverse("token_obtain_pair_view"), self.user_normal_data).data["access"]  # 일반 계정
        self.access_token_admin = self.client.post(reverse("token_obtain_pair_view"), self.user_admin_data).data["access"]  # 어드민 계정

    # 7. 맛집 상세페이지
    def test_place_detail_get_success(self):
        response = self.client.get(
            path=reverse("place_detail_view", kwargs={"place_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_normal}",
        )
        self.assertEqual(response.status_code, 200)

    # 8. 맛집 삭제(어드민 일 때)
    def test_delete_place_success(self):
        response = self.client.delete(
            path=reverse("place_detail_view", kwargs={"place_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_admin}",
        )
        self.assertEqual(response.status_code, 200)

    # 8. 맛집 삭제(어드민이 아닐 때)
    def test_delete_place_fail(self):
        response = self.client.delete(
            path=reverse("place_detail_view", kwargs={"place_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_normal}",
        )
        self.assertEqual(response.status_code, 403)


class PlaceBookmarkAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"username": "test1234", "password": "Test1234!"}
        cls.user = User.objects.create_user("test1234", "test1@test.com", "01012341234", "Test1234!")
        Profile.objects.create(user=cls.user)
        cls.place = Place.objects.create(
            place_name="장소",
            category="한식",
            rating=5,
            place_address="제주시",
            place_time="영업시간",
            place_img="img_url",
        )

    def setUp(self):
        self.access_token = self.client.post(reverse("token_obtain_pair_view"), self.user_data).data["access"]  

    # 9. 장소 북마크
    def test_bookmark_success(self):
        response_execute = self.client.post(
            path=reverse("place_bookmark_view", kwargs={"place_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response_execute.status_code, 200)

        response_cancel = self.client.post(
            path=reverse("place_bookmark_view", kwargs={"place_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response_cancel.status_code, 200)


# 10. 장소 검색
class PlaceSearchAPIViewTestCase(APITestCase):
    def test_search_success(self):
        response = self.client.get(
            path=reverse("search"),
            data={"keyword": "양식"},
        )
        self.assertEqual(response.status_code, 200)

    def test_search_blank_fail(self):
        response = self.client.get(
            path=reverse("search"),
            data={"keyword": ""},
        )
        self.assertEqual(response.status_code, 400)

    def test_search_query_fail(self):
        response = self.client.get(
            path=reverse("search"),
            data={"xeyword": ""},
        )
        self.assertEqual(response.status_code, 400)