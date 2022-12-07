from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import generics

from django.shortcuts import get_list_or_404

from drf_yasg.utils import swagger_auto_schema

from gaggamagga.permissions import IsAdminOrOntherReadOnly
from . import client
from .models import Place
from .serializers import PlaceSelectSerializer, PlaceSerializer, PlaceCreateSerializer

from .rcm_places import rcm_place

from django.db.models import Case, Q, When

FOOD_CATEGORY = (
        ('F1', '분식'),
        ('F2', '한식'),
        ('F3', '돼지고기구이'),
        ('F4', '치킨,닭강정'),
        ('F5', '햄버거'),
        ('F6', '피자'),
        ('F7', '중식당'),
        ('F8', '일식당'),
        ('F9', '양식'),
        ('F10', '태국음식'),
        ('F11', '인도음식'),
        ('F12', '베트남음식'),
    )

##### 취향 선택 #####
class PlaceSelectView(APIView):
    permission_class = [IsAuthenticated]

    #맛집 취향 선택
    def get(self, request):
        place = []
        for i in range(len(FOOD_CATEGORY)):
            pick = Place.objects.filter(category=FOOD_CATEGORY[i][1]).order_by('-rating')[0]
            place.append(pick)
        serializer = PlaceSelectSerializer(place, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


##### 장소 #####
class PlaceListView(APIView):
    permission_classes = [IsAdminOrOntherReadOnly]

    #맛집 전체 리스트
    @swagger_auto_schema(operation_summary="맛집 전체 리스트",
                    responses={200 : '성공', 500 : '서버 에러'})
    #맛집 리스트
    def get(self, request, place_id):
        place_list = rcm_place(user_id = request.user.id, picked_place_id=place_id)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(place_list)])
        place = Place.objects.filter(id__in=place_list).order_by(preserved)
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

class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **wsargs):
        query = request.GET.get('q')
        if not query:
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        results = client.perform_search(query)
        return Response(results)

class SearchListOldView(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Place.objects.none()
        if q is not None:
            results = qs.search(q)
        return results