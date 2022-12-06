from django.shortcuts import render
from django.shortcuts import get_list_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework import generics

from drf_yasg.utils import swagger_auto_schema

from places .models import Place
from places.serializers import PlaceSerializer
from . import client


from gaggamagga.permissions import IsAdminOrOntherReadOnly
from .models import Place
from .serializers import PlaceLocationSelectSerializer, PlaceSerializer, PlaceCreateSerializer

##### 장소 #####
class PlaceListView(APIView):
    permission_classes = [IsAdminOrOntherReadOnly]

    #맛집 전체 리스트
    @swagger_auto_schema(operation_summary="맛집 전체 리스트",
                    responses={200 : '성공', 500 : '서버 에러'})
    def get(self, request):
        place = Place.objects.all()
        serializer = PlaceSerializer(place, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #맛집 생성
    @swagger_auto_schema(request_body=PlaceCreateSerializer, 
                    operation_summary="맛집 생성",
                    responses={200 : '성공', 400 : '인풋값 에러', 500 : '서버 에러'})
    def post(self, request):
        serializer = PlaceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlaceDetailView(APIView):
    permission_classes = [IsAdminOrOntherReadOnly]

    #맛집 상세 페이지
    @swagger_auto_schema(operation_summary="맛집 상세 페이지",
                    responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def get(self, request, place_id):
        place = get_object_or_404(Place, id=place_id)
        place.hit_count
        serializer = PlaceSerializer(place)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #맛집 수정
    @swagger_auto_schema(request_body=PlaceCreateSerializer, 
                    operation_summary="맛집 수정",
                    responses={200 : '성공', 400 : '인풋값 에러', 404: '찾을 수 없음' ,500 : '서버 에러'})
    def put(self, request, place_id):
        place = get_object_or_404(Place, id=place_id)
        serializer = PlaceCreateSerializer(place, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #맛집 삭제
    @swagger_auto_schema(operation_summary="맛집 삭제",
                    responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def delete(self, request, place_id):
        place = get_object_or_404(Place, id=place_id)
        place.delete()
        return Response({"message":"맛집 삭제 완료"},status=status.HTTP_200_OK)

class PlaceBookmarkView(APIView):
    permission_classes = [IsAuthenticated] 

    # 장소 북마크
    @swagger_auto_schema(operation_summary="장소 북마크",  
                responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def post(self, request, place_id):
        place = get_object_or_404(Place, id=place_id)
        if request.user in place.place_bookmark.all():
            place.place_bookmark.remove(request.user)
            return Response({"message":"북마크를 취소했습니다."}, status=status.HTTP_200_OK)
        else:
            place.place_bookmark.add(request.user)
            return Response({"message":"북마크를 했습니다."}, status=status.HTTP_200_OK)

### Place Select ###
class PlaceLocationSelectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        place = get_list_or_404(Place)
        serializer = PlaceLocationSelectSerializer(place, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


### Recommend Place ###
class RecommendPlaceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        place = get_list_or_404(Place)
        serializer = PlaceLocationSelectSerializer(place, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchListView(generics.GenericAPIView) :
    def get(self, request, *args, **wsargs) :
        query = request.GET.get('q')
        if not query :
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        results = client.perform_search(query)
        return Response(results)

class SearchListOldView(generics.ListAPIView) :
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_queryset(self, *args, **kwargs) :
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Place.objects.none()
        if q is not None:
            results = qs.search(q)
        return results