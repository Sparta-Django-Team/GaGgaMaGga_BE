from rest_framework.test import APITestCase

from django.urls import reverse
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY

from users.models import User, Profile
from places.models import Place
from .models import Review, Comment, Recomment, Report

from PIL import Image
import tempfile

def get_temporary_image(temp_file):
    size = (200,200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file

#### 리뷰 ####
# 전체 리뷰 조회
class ReviewRankAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username':'test1234', 'password':'Test1234!'}
        cls.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        Profile.objects.create(user=cls.user)
        cls.place = Place.objects.create(place_name="장소명", category="카테고리", rating="5", place_address="주소", place_time="시간", place_img="이미지")

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair_view'), self.user_data).data['access']
    
    # 전체 리뷰 조회 성공
    def test_review_rank_list_success(self):  
        response = self.client.get(
            path=reverse("reveiw_rank_view"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.assertEqual(response.status_code, 200)

# 리뷰 조회/작성
class ReviewAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username':'test1234', 'password':'Test1234!'}
        cls.review_data = {'content':'some content', "rating_cnt": "5"}
        cls.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        Profile.objects.create(user=cls.user)
        cls.place = Place.objects.create(place_name="장소명", category="카테고리", rating="5", place_address="주소", place_time="시간", place_img="이미지")

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair_view'), self.user_data).data['access']
    
    # 해당 맛집 리뷰 조회 성공
    def test_review_list_success(self):  
        response = self.client.get(
            path=reverse("review_list_view", kwargs={'place_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.assertEqual(response.status_code, 200)

    #리뷰 작성 성공
    def test_review_create_success(self):  
        response = self.client.post(
            path=reverse("review_list_view", kwargs={'place_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.review_data)
        self.assertEqual(response.status_code, 201)

    # 이미지 포함 리뷰 작성 성공
    def test_create_review_with_image(self):
        # 첫번째 이미지
        # 임시 이미지 파일 생성
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)  # 첫번째 프레임을 받아옴
        self.review_data["review_image_one"] = image_file
        # 두번째 이미지
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)  
        self.review_data["review_image_two"] = image_file
        # 세번째 이미지
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0) 
        self.review_data["review_image_three"] = image_file

        # 전송
        response = self.client.post(
            path=reverse("review_list_view", kwargs={'place_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            content_type=MULTIPART_CONTENT,
            data=encode_multipart(data = self.review_data, boundary=BOUNDARY)
        )
        self.assertEqual(response.status_code, 201)

    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_review_post(self):
        response = self.client.post(
            path=reverse("review_list_view", kwargs={'place_id':1}), 
            data=self.review_data)
        self.assertEqual(response.status_code, 401)
    
    # 리뷰 작성 실패(리뷰내용이 빈칸)
    def test_review_create_content_fail(self):  
        response = self.client.post(
            path=reverse("review_list_view", kwargs={'place_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data= {'content':'', "rating_cnt": "4"})
        self.assertEqual(response.status_code, 400)

    # 리뷰 작성 실패(리뷰평점이 빈칸)
    def test_review_create_rating_fail(self):  
        response = self.client.post(
            path=reverse("review_list_view", kwargs={'place_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data= {'content':'some content', "rating_cnt": ""})
        self.assertEqual(response.status_code, 400)

# 리뷰 수정/삭제/신고
class ReviewDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_data = {'username':'test1234', 'password':'Test1234!'}
        cls.user2_data = {'username':'test1235', 'password':'Test1234!'}
        cls.user3_data = {'username':'test1236', 'password':'Test1234!'}
        cls.review_data = {'content':'some content', "rating_cnt": "5"}
        cls.edit_review_data={'content':'edit content', "rating_cnt": "5"}
        cls.report_data = {'content':'report content', "category": '욕설이 들어갔어요.'}
        cls.user1 = User.objects.create_user("test1234","test1@test.com", "01012341234","Test1234!")
        cls.user2 = User.objects.create_user("test1235","test2@test.com", "01012341235","Test1234!")
        cls.user3 = User.objects.create_user("test1236","test3@test.com", "01012341236","Test1234!")
        Profile.objects.create(user=cls.user1, review_cnt=1)
        Profile.objects.create(user=cls.user2)
        Profile.objects.create(user=cls.user3)
        cls.place = Place.objects.create(place_name="장소명", rating="5", category="카테고리", place_address="주소", place_time="시간", place_img="이미지")
        cls.review = Review.objects.create(content="내용", rating_cnt="5", author=cls.user1, place=cls.place)
        cls.review2 = Review.objects.create(content="내용", rating_cnt="5", author=cls.user1, place=cls.place)
        cls.report = Report.objects.create(content="신고내용", category='욕설이 들어갔어요.', author=cls.user2, review=cls.review2)

    def setUp(self):
        self.access_token_1 = self.client.post(reverse('token_obtain_pair_view'), self.user1_data).data['access']
        self.access_token_2 = self.client.post(reverse('token_obtain_pair_view'), self.user2_data).data['access']
        self.access_token_3 = self.client.post(reverse('token_obtain_pair_view'), self.user3_data).data['access']

    # 해당 리뷰 조회 성공
    def test_review_detail_success(self):  
        response = self.client.get(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}")
        self.assertEqual(response.status_code, 200)

    #리뷰 수정 성공
    def test_review_edit_success(self):  
        response = self.client.put(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data={'content':'edit content', "rating_cnt": "5"})
        self.assertEqual(response.status_code, 200)

    # 이미지 포함 리뷰 수정 성공
    def test_edit_review_with_image(self):
        # 첫번째 이미지
        # 임시 이미지 파일 생성
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)  # 첫번째 프레임을 받아옴
        self.edit_review_data["review_image_one"] = image_file
        # 두번째 이미지
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)  
        self.edit_review_data["review_image_two"] = image_file
        # 세번째 이미지
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0) 
        self.edit_review_data["review_image_three"] = image_file

        # 전송
        response = self.client.put(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            content_type=MULTIPART_CONTENT,
            data=encode_multipart(data=self.edit_review_data, boundary=BOUNDARY)
        )
        self.assertEqual(response.status_code, 200)

    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_review_pup(self):
        response = self.client.put(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}), 
            data=self.review_data)
        self.assertEqual(response.status_code, 401)

    # 리뷰 수정 실패(리뷰내용이 빈칸)
    def test_review_edit_content_fail(self):  
        response = self.client.put(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data= {'content':'', "rating_cnt": "5"})
        self.assertEqual(response.status_code, 400)
    
    # 리뷰 수정 실패(리뷰평점이 빈칸)
    def test_review_edit_rating_fail(self):  
        response = self.client.put(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data= {'content':'edit content', "rating_cnt": ""})
        self.assertEqual(response.status_code, 400)

    # 리뷰 수정 실패(리뷰작성자 불일치(작성자 user1))
    def test_review_edit_author_fail(self):
        response = self.client.put(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data= {'content':'edit content', "rating_cnt": "5"})
        self.assertEqual(response.status_code, 403)

    # 리뷰 삭제 성공
    def test_review_delete_success(self): 
        response = self.client.delete(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data=self.review_data)
        self.assertEqual(response.status_code, 200)

    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_review_delete(self):
        response = self.client.delete(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}), 
            data=self.review_data)
        self.assertEqual(response.status_code, 401)

    # 리뷰 삭제 실패(리뷰작성자 불일치(작성자 user1))
    def test_review_delete_fail(self):  
        response = self.client.delete(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data=self.review_data)
        self.assertEqual(response.status_code, 403)

    # 리뷰 신고 성공
    def test_review_report_success(self):  
        response = self.client.post(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_3}",
            data=self.report_data)
        self.assertEqual(response.status_code, 200)
    
    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_review_report(self):
        response = self.client.post(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}), 
            data=self.report_data)
        self.assertEqual(response.status_code, 401)
        
    # 리뷰 신고 실패(작성자가 신고)
    def test_review_same_author_report_fail(self):  
        response = self.client.post(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data=self.report_data)
        self.assertEqual(response.status_code, 400)

    # 리뷰 신고 실패(중복 데이터)
    def test_review_report_already_reported_fail(self):  
        response = self.client.post(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':2}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data=self.report_data)
        self.assertEqual(response.status_code, 208)

    # 리뷰 신고 실패(신고 내용 빈칸)
    def test_review_report_content_fail(self):  
        response = self.client.post(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data={'content':'', "category": '욕설이 들어갔어요.'})
        self.assertEqual(response.status_code, 400)

    # 리뷰 신고 실패(신고 카테고리 빈칸)
    def test_review_report_category_fail(self):  
        response = self.client.post(
            path=reverse("review_detail_view", kwargs={'place_id':1, 'review_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data={'content':'report content', "category": ''})
        self.assertEqual(response.status_code, 400)

# 리뷰 좋아요
class ReviewLikeAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username':'test1234', 'password':'Test1234!'}
        cls.review_data = {'content':'some content', "rating_cnt": "5"}
        cls.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        Profile.objects.create(user=cls.user)
        cls.place = Place.objects.create(place_name="장소명", category="카테고리", rating="5", place_address="주소", place_time="시간", place_img="이미지")
        cls.review = Review.objects.create(content="내용", rating_cnt="5", author=cls.user, place=cls.place)

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair_view'), self.user_data).data['access']

    # 리뷰 좋아요 성공
    def test_review_like_success(self):  
        response = self.client.post(
            path=reverse("review_like_view", kwargs={'review_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.review_data)
        self.assertEqual(response.status_code, 200)
    
    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_review_like(self):
        response = self.client.post(
            path=reverse("review_like_view", kwargs={'review_id':1}),
            data=self.review_data)
        self.assertEqual(response.status_code, 401)

#### 댓글 ####
# 댓글 조회/작성
class CommentAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username':'test1234', 'password':'Test1234!'}
        cls.comment_data = {'content':'some content'}
        cls.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        Profile.objects.create(user=cls.user)
        cls.place = Place.objects.create(place_name="장소명", category="카테고리", rating="5", place_address="주소", place_time="시간", place_img="이미지")
        Review.objects.create(content="내용", rating_cnt="5", author=cls.user, place=cls.place)

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair_view'), self.user_data).data['access']

    # 해당 리뷰의 댓글 조회 성공
    def test_commnet_list_success(self):  
        response = self.client.get(
            path=reverse("comment_list_view", kwargs={'review_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.assertEqual(response.status_code, 200)

    # 댓글 작성 성공
    def test_comment_create_success(self):  
        response = self.client.post(
                path=reverse("comment_list_view", kwargs={'review_id':1}),
                HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
                data=self.comment_data)
        self.assertEqual(response.status_code, 201)

    # 로그인 안된 유저가 시도했을때 에러나오는지
    def test_fail_if_not_logged_in_comment_post(self):
        response = self.client.post(
            path=reverse("comment_list_view", kwargs={'review_id':1}), 
            data=self.comment_data)
        self.assertEqual(response.status_code, 401)
    
    # 댓글 작성 실패(댓글내용이 빈칸)
    def test_comment_create_fail(self):  
        response = self.client.post(
                path=reverse("comment_list_view", kwargs={'review_id':1}),
                HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
                data={'content':''})
        self.assertEqual(response.status_code, 400)

# 댓글 수정/삭제
class CommentDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_data = {'username':'test1234', 'password':'Test1234!'}
        cls.user2_data = {'username':'test1235', 'password':'Test1234!'}
        cls.user3_data = {'username':'test1236', 'password':'Test1234!'}
        cls.comment_data = {'content':'some content'}
        cls.report_data = {'content':'report content', "category": '욕설이 들어갔어요.'}
        cls.user1 = User.objects.create_user("test1234","test1@test.com", "01012341234","Test1234!")
        cls.user2 = User.objects.create_user("test1235","test2@test.com", "01012341235","Test1234!")
        cls.user3 = User.objects.create_user("test1236","test3@test.com", "01012341236","Test1234!")
        Profile.objects.create(user=cls.user1)
        Profile.objects.create(user=cls.user2)
        Profile.objects.create(user=cls.user3)
        cls.place = Place.objects.create(place_name="장소명", category="카테고리", rating="5", place_address="주소", place_time="시간", place_img="이미지")
        cls.review = Review.objects.create(content="내용", rating_cnt="5", author=cls.user1, place=cls.place)
        cls.comment = Comment.objects.create(content="내용", author=cls.user1, review=cls.review)
        cls.comment2 = Comment.objects.create(content="내용", author=cls.user1, review=cls.review)
        cls.report = Report.objects.create(content="신고내용", category='욕설이 들어갔어요.', author=cls.user2, comment=cls.comment2)
        

    def setUp(self):
        self.access_token_1 = self.client.post(reverse('token_obtain_pair_view'), self.user1_data).data['access']
        self.access_token_2 = self.client.post(reverse('token_obtain_pair_view'), self.user2_data).data['access']
        self.access_token_3 = self.client.post(reverse('token_obtain_pair_view'), self.user3_data).data['access']

    # 댓글 수정 성공
    def test_comment_edit_success(self):  
        response = self.client.put(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data={'content':'edit content'})
        self.assertEqual(response.status_code, 200)

    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_comment_put(self):
        response = self.client.put(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':1}), 
            data=self.comment_data)
        self.assertEqual(response.status_code, 401)

    # 댓글 수정 실패(댓글수정내용이 빈칸)
    def test_comment_edit_content_fail(self):  
        response = self.client.put(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data= {'content':''})
        self.assertEqual(response.status_code, 400)
    
    # 댓글 수정 실패(리뷰작성자 불일치(작성자 user1))
    def test_comment_edit_author_fail(self):
        response = self.client.put(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data= {'content':'edit content'})
        self.assertEqual(response.status_code, 403)

    # 댓글 삭제 성공
    def test_comment_delete_success(self): 
        response = self.client.delete(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data=self.comment_data)
        self.assertEqual(response.status_code, 200)

    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_comment_delete(self):
        response = self.client.delete(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':1}), 
            data=self.comment_data)
        self.assertEqual(response.status_code, 401)

    # 댓글 삭제 실패(댓글작성자(user1)와 삭제유저(user2)불일치)
    def test_comment_delete_fail(self): 
        response = self.client.delete(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data=self.comment_data)
        self.assertEqual(response.status_code, 403)

    # 댓글 신고 성공
    def test_comment_report_success(self):  
        response = self.client.post(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_3}",
            data=self.report_data)
        self.assertEqual(response.status_code, 200)
    
    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_comment_report(self):
        response = self.client.post(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':1}), 
            data=self.report_data)
        self.assertEqual(response.status_code, 401)
        
    # 댓글 신고 실패(작성자가 신고)
    def test_comment_same_author_report_fail(self):  
        response = self.client.post(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':2}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data=self.report_data)
        self.assertEqual(response.status_code, 400)

    # 댓글 신고 실패(중복 데이터)
    def test_comment_report_already_reported_fail(self):  
        response = self.client.post(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':2}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data=self.report_data)
        self.assertEqual(response.status_code, 208)

    # 댓글 신고 실패(신고 내용 빈칸)
    def test_comment_report_content_fail(self):  
        response = self.client.post(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data={'content':'', "category": '욕설이 들어갔어요.'})
        self.assertEqual(response.status_code, 400)

    # 댓글 신고 실패(신고 카테고리 빈칸)
    def test_comment_report_category_fail(self):  
        response = self.client.post(
            path=reverse("comment_detail_view", kwargs={'review_id':1, 'comment_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data={'content':'report content', "category": ''})
        self.assertEqual(response.status_code, 400)

# 댓글 좋아요
class CommentLikeAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username':'test1234', 'password':'Test1234!'}
        cls.comment_data = {'content':'some content'}
        cls.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        Profile.objects.create(user=cls.user)
        cls.place = Place.objects.create(place_name="장소명", category="카테고리", rating="5", place_address="주소", place_time="시간", place_img="이미지")
        cls.review = Review.objects.create(content="내용", rating_cnt="5", author=cls.user, place=cls.place)
        Comment.objects.create(content="내용", author=cls.user, review=cls.review)

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair_view'), self.user_data).data['access']

    # 댓글 좋아요 성공
    def test_comment_like_success(self):  
        response = self.client.post(
            path=reverse("comment_like_view", kwargs={'comment_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.comment_data)
        self.assertEqual(response.status_code, 200)
    
    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_comment_like(self):
        response = self.client.post(
            path=reverse("comment_like_view", kwargs={'comment_id':1}),
            data=self.comment_data)
        self.assertEqual(response.status_code, 401)

#### 대댓글 ####
# 대댓글 조회/작성
class RecommentAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username':'test1234', 'password':'Test1234!'}
        cls.recomment_data = {'content':'some content'}
        cls.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        Profile.objects.create(user=cls.user)
        cls.place = Place.objects.create(place_name="장소명", category="카테고리", rating="5", place_address="주소", place_time="시간", place_img="이미지")
        cls.review = Review.objects.create(content="내용", rating_cnt="5", author=cls.user, place=cls.place)
        Comment.objects.create(content="내용", author=cls.user, review=cls.review)

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair_view'), self.user_data).data['access']


    # 해당 댓글의 대댓글 조회 성공
    def test_recommnet_list_success(self):  
        response = self.client.get(
            path=reverse("recomment_list_view", kwargs={'review_id':1, 'comment_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.assertEqual(response.status_code, 200)

    # 대댓글 작성 성공
    def test_recomment_create_success(self):  
        response = self.client.post(
                path=reverse("recomment_list_view", kwargs={'review_id':1, 'comment_id':1}),
                HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
                data=self.recomment_data)
        self.assertEqual(response.status_code, 201)

    # 로그인 안된 유저가 시도했을때 에러나오는지
    def test_fail_if_not_logged_in_recomment_post(self):
        response = self.client.post(
            path=reverse("recomment_list_view", kwargs={'review_id':1, 'comment_id':1}),
            data=self.recomment_data)
        self.assertEqual(response.status_code, 401)
    
    # 대댓글 작성 실패(대댓글내용이 빈칸)
    def test_recomment_create_fail(self):  
        response = self.client.post(
                path=reverse("recomment_list_view", kwargs={'review_id':1, 'comment_id':1}),
                HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
                data={'content':''})
        self.assertEqual(response.status_code, 400)

# 대댓글 수정/삭제
class RecommentDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_data = {'username':'test1234', 'password':'Test1234!'}
        cls.user2_data = {'username':'test1235', 'password':'Test1234!'}
        cls.user3_data = {'username':'test1236', 'password':'Test1234!'}
        cls.recomment_data = {'content':'some content'}
        cls.report_data = {'content':'report content', "category": '욕설이 들어갔어요.'}
        cls.user1 = User.objects.create_user("test1234","test1@test.com", "01012341234","Test1234!")
        cls.user2 = User.objects.create_user("test1235","test2@test.com", "01012341235","Test1234!")
        cls.user3 = User.objects.create_user("test1236","test3@test.com", "01012341236","Test1234!")
        Profile.objects.create(user=cls.user1)
        Profile.objects.create(user=cls.user2)
        Profile.objects.create(user=cls.user3)
        cls.place = Place.objects.create(place_name="장소명", category="카테고리", rating="5", place_address="주소", place_time="시간", place_img="이미지")
        cls.review = Review.objects.create(content="내용", rating_cnt="5", author=cls.user1, place=cls.place)
        cls.comment = Comment.objects.create(content="내용", author=cls.user1, review=cls.review)
        cls.recomment = Recomment.objects.create(content="내용", author=cls.user1, comment=cls.comment)
        cls.recomment2 = Recomment.objects.create(content="내용", author=cls.user1, comment=cls.comment)
        cls.report = Report.objects.create(content="신고내용", category='욕설이 들어갔어요.', author=cls.user2, recomment=cls.recomment2)

    def setUp(self):
        self.access_token_1 = self.client.post(reverse('token_obtain_pair_view'), self.user1_data).data['access']
        self.access_token_2 = self.client.post(reverse('token_obtain_pair_view'), self.user2_data).data['access']
        self.access_token_3 = self.client.post(reverse('token_obtain_pair_view'), self.user3_data).data['access']

    # 대댓글 수정 성공
    def test_recomment_edit_success(self):  
        response = self.client.put(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data={'content':'edit content'})
        self.assertEqual(response.status_code, 200)

    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_recomment_put(self):
        response = self.client.put(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':1}),
            data=self.recomment_data)
        self.assertEqual(response.status_code, 401)

    # 대댓글 수정 실패(댓글수정내용이 빈칸)
    def test_recomment_edit_content_fail(self):  
        response = self.client.put(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data= {'content':''})
        self.assertEqual(response.status_code, 400)
    
    # 대댓글 수정 실패(리뷰작성자 불일치(작성자 user1))
    def test_recomment_edit_author_fail(self):
        response = self.client.put(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data= {'content':'edit content'})
        self.assertEqual(response.status_code, 403)

    # 대댓글 삭제 성공
    def test_recomment_delete_success(self): 
        response = self.client.delete(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data= {'content':'edit content'})
        self.assertEqual(response.status_code, 200)

    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_recomment_delete(self):
        response = self.client.delete(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':1}),
            data= {'content':'edit content'})
        self.assertEqual(response.status_code, 401)

    # 대댓글 삭제 실패(대댓글작성자(user1)와 삭제유저(user2)불일치)
    def test_recomment_delete_fail(self): 
        response = self.client.delete(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data= {'content':'edit content'})
        self.assertEqual(response.status_code, 403)

    # 대댓글 신고 성공
    def test_recomment_report_success(self):  
        response = self.client.post(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data=self.report_data)
        self.assertEqual(response.status_code, 200)
    
    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_recomment_report(self):
        response = self.client.post(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':1}),
            data=self.report_data)
        self.assertEqual(response.status_code, 401)
        
    # 댓글 신고 실패(작성자가 신고)
    def test_recomment_same_author_report_fail(self):  
        response = self.client.post(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':1}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data=self.report_data)
        self.assertEqual(response.status_code, 400)

    # 대댓글 신고 실패(중복 데이터)
    def test_recomment_report_already_reported_fail(self):  
        response = self.client.post(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':2}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_2}",
            data=self.report_data)
        self.assertEqual(response.status_code, 208)

    # 대댓글 신고 실패(신고 내용 빈칸)
    def test_recomment_report_content_fail(self):  
        response = self.client.post(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data={'content':'', "category": '욕설이 들어갔어요.'})
        self.assertEqual(response.status_code, 400)

    # 대댓글 신고 실패(신고 카테고리 빈칸)
    def test_recomment_report_category_fail(self):  
        response = self.client.post(
            path=reverse("recomment_detail_view", kwargs={'review_id':1, 'comment_id':1, 'recomment_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token_1}",
            data={'content':'report content', "category": ''})
        self.assertEqual(response.status_code, 400)

# 대댓글 좋아요
class RecommentLikeAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username':'test1234', 'password':'Test1234!'}
        cls.comment_data = {'content':'some content'}
        cls.user = User.objects.create_user("test1234","test@test.com", "01012341234","Test1234!")
        Profile.objects.create(user=cls.user)
        cls.place = Place.objects.create(place_name="장소명", category="카테고리", rating="5", place_address="주소", place_time="시간", place_img="이미지")
        cls.review = Review.objects.create(content="내용", rating_cnt="5", author=cls.user, place=cls.place)
        cls.comment = Comment.objects.create(content="내용", author=cls.user, review=cls.review)
        Recomment.objects.create(content="내용", author=cls.user, comment=cls.comment)

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair_view'), self.user_data).data['access']

    # 대댓글 좋아요 성공
    def test_recomment_like_success(self):  
        response = self.client.post(
            path=reverse("recomment_like_view", kwargs={'recomment_id':1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.comment_data)
        self.assertEqual(response.status_code, 200)
    
    # 로그인 안된 유저가 시도했을때 에러
    def test_fail_if_not_logged_in_recomment_like(self):
        response = self.client.post(
            path=reverse("recomment_like_view", kwargs={'recomment_id':1}),
            data=self.comment_data)
        self.assertEqual(response.status_code, 401)