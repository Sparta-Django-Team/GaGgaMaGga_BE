from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.db.models import Count

from drf_yasg.utils import swagger_auto_schema

from .models import Review, Comment, Recomment, Report
from .serializers import (ReviewListSerializer, ReviewCreateSerializer, ReviewDetailSerializer, 
CommentSerializer, CommentCreateSerializer , RecommentSerializer, RecommentCreateSerializer, ReportSerializer)


#####리뷰#####
class ReviewRankView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(operation_summary="전체 리뷰 조회",
                    responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    #리뷰 전체 리스트
    def get(self, request):

        #최신순
        recent_review = Review.objects.all().order_by('-created_at')

        #좋아요순
        like_count_review = Review.objects.annotate(num_likes=Count('review_like')).order_by('-num_likes','-created_at')

        recent_review_serializer = ReviewListSerializer(recent_review, many=True).data
        like_count_review_serializer = ReviewListSerializer(like_count_review, many=True).data
        
        review = {
            "recent_review": recent_review_serializer,
            "like_count_review": like_count_review_serializer
        }
        return Response(review, status=status.HTTP_200_OK)

class ReviewListView(APIView):
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(),]
        return super(ReviewListView, self).get_permissions()

    #장소 리뷰 리스트
    @swagger_auto_schema(operation_summary="장소 리뷰 리스트",
                    responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def get(self, request, place_id):

        #최신순
        recent_review = Review.objects.filter(place_id=place_id).order_by('-created_at')

        #좋아요순
        like_count_review = Review.objects.filter(place_id=place_id).annotate(num_likes=Count('review_like')).order_by('-num_likes','-created_at')

        recent_review_serializer = ReviewListSerializer(recent_review, many=True).data
        like_count_review_serializer = ReviewListSerializer(like_count_review, many=True).data

        review = {
            "recent_review": recent_review_serializer,
            "like_count_review": like_count_review_serializer
        }
        return Response(review, status=status.HTTP_200_OK)

    #리뷰 작성
    @swagger_auto_schema(request_body=ReviewCreateSerializer,
                    operation_summary="리뷰 작성",
                    responses={201 : '성공', 400:'인풋값 에러', 500 : '서버 에러'})
    def post(self, request, place_id):
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, place_id=place_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(APIView):
    permission_classes = [IsAuthenticated]

    #리뷰 상세 페이지
    @swagger_auto_schema(operation_summary="리뷰 상세 조회",
                    responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #리뷰 수정
    @swagger_auto_schema(request_body=ReviewCreateSerializer,
                    operation_summary="리뷰 작성",
                    responses={201 : '성공', 400:'인풋값 에러', 500 : '서버 에러'})
    def put(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.author:
            serializer = ReviewCreateSerializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(author=request.user, review_id=review_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

    #리뷰 삭제
    @swagger_auto_schema(operation_summary="리뷰 삭제", 
                    responses={201 : '성공', 403:'접근 권한 없음', 404:'찾을 수 없음', 500 : '서버 에러'})
    def delete(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.author:
            review.delete()
            return Response({"message":"리뷰 삭제"}, status=status.HTTP_200_OK)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN) 

    #리뷰 신고
    @swagger_auto_schema(request_body=ReportSerializer, 
                operation_summary="리뷰 신고", 
                responses={ 200 : '성공', 208 : '중복 데이터', 404:'인풋값 에러',  500:'서버 에러'})
    def post(self, request, review_id):
        try :
            Report.objects.get(author=request.user.id, review=review_id)
            return Response({"message":"이미 신고를 한 후기입니다."}, status=status.HTTP_208_ALREADY_REPORTED)
        
        except Report.DoesNotExist:
            serializer = ReportSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, review_id=review_id)
                return Response({"message":"신고가 완료되었습니다."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 리뷰 좋아요
class ReviewLikeView(APIView):
    permission_classes = [IsAuthenticated] 

    @swagger_auto_schema(operation_summary="리뷰 좋아요",  
                    responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.user in review.review_like.all():
            review.review_like.remove(request.user)
            return Response({"message":"리뷰 좋아요를 취소했습니다"}, status=status.HTTP_200_OK)
        else:
            review.review_like.add(request.user)
            return Response({"message":"리뷰 좋아요를 했습니다."}, status=status.HTTP_200_OK)

#####댓글#####
class CommentListView(APIView):
    permission_classes = [IsAuthenticated] 

    # 댓글 조회
    @swagger_auto_schema(operation_summary="댓글 조회",
                    responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        comments = review.review_comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 작성
    @swagger_auto_schema(request_body=CommentCreateSerializer,
                    operation_summary="댓글 작성",
                    responses={201 : '성공', 400:'인풋값 에러', 500 : '서버 에러'})
    def post(self, request, review_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, review_id=review_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated] 
    
    # 댓글 수정
    @swagger_auto_schema(request_body=CommentCreateSerializer, 
                        operation_summary="댓글 수정", 
                        responses={ 200 : '성공', 400:'인풋값 에러', 403:'접근 권한 없음', 404:'찾을 수 없음', 500:'서버 에러'})
    def put(self, request, review_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.author:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, review_id=review_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

    # 댓글 삭제
    @swagger_auto_schema(operation_summary="댓글 삭제", 
                        responses={ 200 : '성공', 403:'접근 권한 없음', 404:'찾을 수 없음', 500:'서버 에러'})
    def delete(self, request, review_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.author:
            comment.delete()
            return Response({"message":"댓글 삭제 완료"},status=status.HTTP_200_OK)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)
    
    #댓글 신고
    @swagger_auto_schema(request_body=ReportSerializer, 
                    operation_summary="댓글 신고", 
                    responses={ 200 : '성공', 208 : '중복 데이터', 404:'인풋값 에러',  500:'서버 에러'})
    def post(self, request, review_id, comment_id):
        try :
            Report.objects.get(author=request.user.id, comment=comment_id)
            return Response({"message":"이미 신고를 한 후기입니다."}, status=status.HTTP_208_ALREADY_REPORTED)
        
        except Report.DoesNotExist:
            serializer = ReportSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, comment=comment_id)
                return Response({"message":"신고가 완료되었습니다."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 댓글 좋아요
class CommentLikeView(APIView):
    permission_classes = [IsAuthenticated] 

    @swagger_auto_schema(operation_summary="댓글 좋아요",  
                    responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.comment_like.all():
            comment.comment_like.remove(request.user)
            return Response({"message":"댓글 좋아요를 취소했습니다"}, status=status.HTTP_200_OK)
        else:
            comment.comment_like.add(request.user)
            return Response({"message":"댓글 좋아요를 했습니다"}, status=status.HTTP_200_OK)

#####대댓글##### 
class RecommentListView(APIView):
    permission_classes = [IsAuthenticated] 

    # 대댓글 조회
    @swagger_auto_schema(operation_summary="대댓글 조회",
                    responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def get(self, request, review_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        recomments = comment.comment_recomments.all()
        serializer = RecommentSerializer(recomments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 대댓글 작성
    @swagger_auto_schema(request_body=RecommentCreateSerializer,
                    operation_summary="대댓글 작성",
                    responses={201 : '성공', 400:'인풋값 에러', 500 : '서버 에러'})
    def post(self, request, review_id, comment_id):
        serializer = RecommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, comment_id=comment_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecommentDetailView(APIView):
    permission_classes = [IsAuthenticated] 

    # 대댓글 수정
    @swagger_auto_schema(request_body=RecommentCreateSerializer, 
                        operation_summary="대댓글 수정", 
                        responses={ 200 : '성공', 400:'인풋값 에러', 403:'접근 권한 없음', 404:'찾을 수 없음', 500:'서버 에러'})
    def put(self, request, review_id, comment_id, recomment_id):
        recomment = get_object_or_404(Recomment, id=recomment_id)
        if request.user == recomment.author:
            serializer = RecommentCreateSerializer(recomment, data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, comment_id=comment_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

    # 대댓글 삭제
    @swagger_auto_schema(operation_summary="대댓글 삭제", 
                        responses={ 200 : '성공', 403:'접근 권한 없음', 404:'찾을 수 없음', 500:'서버 에러'})
    def delete(self, request, review_id, comment_id, recomment_id):
        recomment = get_object_or_404(Recomment, id=recomment_id)
        if request.user == recomment.author:
            recomment.delete()
            return Response({"message":"대댓글 삭제 완료"},status=status.HTTP_200_OK)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)
    
    #대댓글 신고
    @swagger_auto_schema(request_body=ReportSerializer, 
            operation_summary="대댓글 신고", 
            responses={ 200 : '성공', 208 : '중복 데이터', 404:'인풋값 에러',  500:'서버 에러'})
    def post(self, request,review_id, comment_id, recomment_id):
        try :
            Report.objects.get(author=request.user.id, recomment=recomment_id)
            return Response({"message":"이미 신고를 한 후기입니다."}, status=status.HTTP_208_ALREADY_REPORTED)
        
        except Report.DoesNotExist:
            serializer = ReportSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, recomment=recomment_id)
                return Response({"message":"신고가 완료되었습니다."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 대댓글 좋아요
class RecommentLikeView(APIView):
    permission_classes = [IsAuthenticated] 

    @swagger_auto_schema(operation_summary="대댓글 좋아요",  
                    responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def post(self, request, recomment_id):
        recomment = get_object_or_404(Recomment, id=recomment_id)
        if request.user in recomment.recomment_like.all():
            recomment.recomment_like.remove(request.user)
            return Response("대댓글 좋아요취소했습니다.", status=status.HTTP_200_OK)
        else:
            recomment.recomment_like.add(request.user)
            return Response("대댓글 좋아요했습니다.", status=status.HTTP_200_OK)
