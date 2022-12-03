from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from reviews.models import Review, Comment
from places.models import Place

from reviews.serializers import (ReviewListSerializer,ReviewCreateSerializer, CommentSerializer, CommentCreateSerializer)


class ReviewView(APIView):
    #장소리뷰리스트
    permissions_classes = [IsAuthenticated] 
    def get(self,request,place_id):
        review = Review.objects.filter(place_id=place_id)
        serializer = ReviewListSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #리뷰작성
    def post(self, request, place_id):
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, place_id=place_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 댓글 
class CommentView(APIView):
    permissions_classes = [IsAuthenticated] 

    # 댓글 조회
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        comments = review.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # 댓글 작성
    def post(self, request, review_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, review_id=review_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permissions_classes = [IsAuthenticated] 

    # 댓글 수정
    def put(self, request, review_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, review_id=review_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)
    # 댓글 삭제
    def delete(self, request, review_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message":"댓글 삭제 완료"},status=status.HTTP_200_OK)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)