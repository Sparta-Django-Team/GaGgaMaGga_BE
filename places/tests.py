<<<<<<< HEAD
from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User, Profile
from places.models import Place
=======
from rest_framework.test import APITestCase

from django.urls import reverse

from users.models import User, Profile
from reviews.models import Review, Comment, Recomment, Report
from .models import Place

import random
'''
사용자 Case
- 비로그인 계정
- 로그인 계정(리뷰x)
- 로그인 계정(리뷰O)

테스트 케이스
# 비로그인 계정, 로그인 계정(리뷰X), 카카오계정(리뷰X)
1. 카테고리 선택(place_preference.html, 음식 선택)
2. 카테고리 선택(place_preference.html, 장소 선택)
3. 장소 리스트 불러오기(place_list.html, index에서 음식 선택 > 선호도 선택 - 한식, 패스트푸드, 중식, 일식, 양식, 아시아)
4. 장소 리스트 불러오기(place_list.html, index에서 장소 선택 > 선호도 선택 - 제주시, 서귀포시)

# 로그인 계정(리뷰O), 카카오계정(리뷰O)
5. 장소 리스트 불러오기(place_list.html, index에서 음식 선택 - 한식, 패스트푸드, 중식, 일식, 양식, 아시아)
6. 장소 리스트 불러오기(place_list.html, index에서 장소 선택 - 제주시, 서귀포시)

# 공통
7. 맛집 상세페이지
8. 맛집 북마크(유저일 때)
9. 검색

# 어드민 계정
10. 맛집 삭제 (어드민 일 때, 어드민이 아닐 때)

# Place
path('<int:place_id>/', views.PlaceDetailView.as_view(), name='place_detail_view'),
path('<int:place_id>/bookmarks/',views.PlaceBookmarkView.as_view(), name='place_bookmark_view'),

#Recommendation
path('selection/<int:choice_no>/', views.PlaceSelectView.as_view(), name="place_select_view"),
path('new/<int:place_id>/<str:category>/', views.NewUserPlaceListView.as_view(), name='new_user_place_list_view'),
path('list/<int:cate_id>/', views.UserPlaceListView.as_view(), name='user_place_list_view'),

# Search
path('search/', views.SearchListView.as_view(), name='search'),

'''

CHOICE_CATEGORY = (
        ('1', '분식'),
        ('2', '한식'),
        ('3', '돼지고기구이'),
        ('4', '치킨,닭강정'),
        ('5', '햄버거'),
        ('6', '피자'),
        ('7', '중식'),
        ('8', '일식'),
        ('9', '양식'),
        ('10', '태국음식'),
        ('11', '인도음식'),
        ('12', '베트남음식'),
        ('13', '제주시'),
        ('14', '서귀포시'),
    )
>>>>>>> main



#### 장소 ####
<<<<<<< HEAD
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
=======
class PlaceSelectAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # cls.user_data = {'username':'test1234', 'password':'Test1234!'}
        # cls.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        # Profile.objects.create(user=cls.user)
        cls.place = Place.objects.create(place_name="장소01", category="분식", rating="5", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소02", category="한식", rating="5", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소03", category="돼지고기구이", rating="5", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소04", category="치킨,닭강정", rating="3", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소05", category="햄버거", rating="4", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소06", category="피자", rating="5", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소07", category="중식", rating="3", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소08", category="일식", rating="5", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소09", category="양식", rating="3", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소10", category="태국음식", rating="2", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소11", category="인도음식", rating="4", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소12", category="베트남음식", rating="3", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소13", category="분식", rating="5", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소14", category="한식", rating="5", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소15", category="돼지고기구이", rating="5", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소16", category="치킨,닭강정", rating="4", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소17", category="햄버거", rating="5", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소18", category="피자", rating="2", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소19", category="중식", rating="4", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소20", category="일식", rating="4", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소21", category="양식", rating="5", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소22", category="태국음식", rating="5", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소23", category="인도음식", rating="4", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소24", category="베트남음식", rating="2", place_address="서귀포시", place_time="시간", place_img="이미지")
        print("---장소 등록 완료1---\n")
        for i in range(30):
            cls.user = User.objects.create_user(f"user{i+1}",f"user{i+1}@test.com","01000000000","Test1234!")
        print("---유저 등록 완료1---\n")
        for i in range(100):  
            cls.review = Review.objects.create(content="some content", rating_cnt = random.randint(1, 5), author=cls.user, place_id=random.randint(1, 24))
        print("---리뷰 등록 완료1---\n")

    # 1. [비로그인] 카테고리 선택(place_preference.html, 음식 선택)
    def test_place_select1(self):
        category_no1 = random.randint(1, 12)
        response = self.client.get(
            path=reverse("place_select_view", kwargs={'choice_no':category_no1}))
        self.assertEqual(response.status_code, 200)
        print("---카테고리 선택 1---\n")

    # 2. [비로그인] 카테고리 선택(place_preference.html, 장소 선택)
    def test_place_select2(self):
        category_no2 = random.randint(13, 14)
        response = self.client.get(
            path=reverse("place_select_view", kwargs={'choice_no':category_no2}))
        self.assertEqual(response.status_code, 200)
        print("---카테고리 선택 2---\n")


# 3/4. [비로그인] 장소 리스트 불러오기(place_list.html, index에서 음식/장소 선택 > 선호도 선택)
class PlaceListAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # cls.user_data = {'username':'test1234', 'password':'Test1234!'}
        # cls.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        # Profile.objects.create(user=cls.user)
        cls.place = Place.objects.create(place_name="장소01", category="분식", rating="5", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소02", category="한식", rating="5", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소03", category="돼지고기구이", rating="5", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소04", category="치킨,닭강정", rating="3", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소05", category="햄버거", rating="4", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소06", category="피자", rating="5", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소07", category="중식", rating="3", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소08", category="일식", rating="5", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소09", category="양식", rating="3", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소10", category="태국음식", rating="2", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소11", category="인도음식", rating="4", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소12", category="베트남음식", rating="3", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소13", category="분식", rating="5", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소14", category="한식", rating="5", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소15", category="돼지고기구이", rating="5", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소16", category="치킨,닭강정", rating="4", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소17", category="햄버거", rating="5", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소18", category="피자", rating="2", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소19", category="중식", rating="4", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소20", category="일식", rating="4", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소21", category="양식", rating="5", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소22", category="태국음식", rating="5", place_address="서귀포시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소23", category="인도음식", rating="4", place_address="제주시", place_time="시간", place_img="이미지")
        cls.place = Place.objects.create(place_name="장소24", category="베트남음식", rating="2", place_address="서귀포시", place_time="시간", place_img="이미지")
        print("---장소 등록 완료2---\n")
        for i in range(30):
            cls.user = User.objects.create_user(f"user{i+1}",f"user{i+1}@test.com","01000000000","Test1234!")
        print("---유저 등록 완료2---\n")
        for i in range(100):  
            cls.review = Review.objects.create(content="some content", rating_cnt = random.randint(1, 5), author=cls.user, place_id=random.randint(1, 24))
        print("---리뷰 등록 완료2---\n")

    
    # 음식 선택(1~12)
    def test_place_list1(self):        # 분식
        place_id = 1
        category = CHOICE_CATEGORY[0][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---음식 선택 1---\n")

    def test_place_list2(self):        # 한식
        place_id = 2
        category = CHOICE_CATEGORY[1][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---음식 선택 2---\n")

    def test_place_list3(self):        # 돼지고기구이
        place_id = 3
        category = CHOICE_CATEGORY[2][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---음식 선택 3---\n")

    def test_place_list4(self):        # 치킨,닭강정
        place_id = 4
        category = CHOICE_CATEGORY[3][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---음식 선택 4---\n")

    def test_place_list5(self):        # 햄버거
        place_id = 5
        category = CHOICE_CATEGORY[4][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---음식 선택 5---\n")

    def test_place_list6(self):        # 피자
        place_id = 6
        category = CHOICE_CATEGORY[5][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---음식 선택 6---\n")

    def test_place_list7(self):        # 중식
        place_id = 7
        category = CHOICE_CATEGORY[6][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---음식 선택 7---\n")

    def test_place_list8(self):        # 일식
        place_id = 8
        category = CHOICE_CATEGORY[7][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---음식 선택 8---\n")

    def test_place_list9(self):        # 양식
        place_id = 9
        category = CHOICE_CATEGORY[8][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---음식 선택 9---\n")

    def test_place_list10(self):        # 태국음식
        place_id = 10
        category = CHOICE_CATEGORY[9][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---음식 선택 10---\n")

    def test_place_list11(self):        # 인도음식
        place_id = 11
        category = CHOICE_CATEGORY[10][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---음식 선택 11---\n")

    def test_place_list12(self):        # 베트남음식
        place_id = 12
        category = CHOICE_CATEGORY[11][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---음식 선택 12---\n")

    # 장소 선택(13~14)
    def test_place_list13(self):        # 제주시
        place_id = 13
        category = CHOICE_CATEGORY[12][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---장소 선택 13---\n")

    def test_place_list14(self):        # 서귀포시
        place_id = 14
        category = CHOICE_CATEGORY[13][1]
        response = self.client.get(
            path=reverse("new_user_place_list_view", kwargs={'place_id':place_id, 'category':category}))
        self.assertEqual(response.status_code, 200)
        print("---장소 선택 14---\n")



# class PlaceBookmarkAPIViewTestCase(APITestCase):
#     def setUp(self):
#         self.user1 = User.objects.create_user("test12341","test1@test.com", "01012351234","Test1234!")

#         self.profile1 = Profile.objects.create(user=self.user1, nickname="test", intro='test')
        
#         self.user = {"username": "test12341", "password":"Test1234!"}
        
#     def test_follow_success(self):
#         access_token = self.client.post(reverse('token_obtain_pair_view'), self.user).data['access']
#         response_case_1 = self.client.post(
#             path=reverse("process_follow_view", kwargs={"nickname":"test1"}),
#             HTTP_AUTHORIZATION=f"Bearer {access_token}",
#         )
        
#         self.assertEqual(response_case_1.status_code, 200)
        
#         response_case_2 = self.client.post(
#             path=reverse("process_follow_view", kwargs={"nickname":"test1"}),
#             HTTP_AUTHORIZATION=f"Bearer {access_token}",
#         )
#         self.assertEqual(response_case_2.status_code, 200)
>>>>>>> main
