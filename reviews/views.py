from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from reviews.models import Review
from places.models import Place

from reviews.serializers import ReviewListSerializer,ReviewCreateSerializer


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

