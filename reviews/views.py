from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from reviews.models import Review
from places.models import Place

from reviews.serializers import (ReviewListSerializer,ReviewCreateSerializer,ReviewDetailSerializer)


class ReviewLoadView(APIView):
    #장소리뷰리스트
    permissions_classes = [IsAuthenticated] 
    def get(self,request,place_id):
        review = Review.objects.filter(place_id=place_id)
        serializer = ReviewListSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReviewCreateView(APIView):
    #리뷰작성
    def post(self, request, place_id):
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, place_id=place_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(APIView):
    permissions_classes = [AllowAny]

    #리뷰상세페이지
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #리뷰 수정
    def put(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            serializer = ReviewCreateSerializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(user=request.user, review_id=review_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)
