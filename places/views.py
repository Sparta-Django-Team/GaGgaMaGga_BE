from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework import generics

from django.db.models import Case, When

from drf_yasg.utils import swagger_auto_schema

from gaggamagga.permissions import IsAdminOrOntherReadOnly
from . import client
from .models import Place
from .serializers import PlaceSelectSerializer, PlaceSerializer
from .rcm_places import rcm_place_user, rcm_place_new_user

CHOICE_CATEGORY = (
        ('1', '분식'),
        ('2', '한식'),
        ('3', '돼지고기구이'),
        ('4', '치킨,닭강정'),
        ('5', '햄버거'),
        ('6', '피자'),
        ('7', '중식당'),
        ('8', '일식당'),
        ('9', '양식'),
        ('10', '태국음식'),
        ('11', '인도음식'),
        ('12', '베트남음식'),
        ('13', '강남'),
    )

##### 취향 선택 #####
class PlaceSelectView(APIView):
    permission_classes = [AllowAny]
    
    #맛집 취향 선택(리뷰가 없거나, 비로그인 계정일 경우)
    def get(self, request, choice_no):
        place_list = []
        
        # Case1: choice place location
        if choice_no > 12:
            place_list = []
            for i in range(0, 12):
                pick = Place.objects.filter(place_address__contains=CHOICE_CATEGORY[choice_no-1][1],category=CHOICE_CATEGORY[i][1]).first()
                place_list.append(pick.id)
            
            # Create list for custom sorting
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(place_list)])
            place = Place.objects.filter(id__in=place_list).order_by(preserved)
            serializer = PlaceSelectSerializer(place, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Case2: choice food group
        else:
            if (choice_no == 3)|(choice_no == 6)|(choice_no == 12):
                # Merge queryset for 3categories
                place_list = []
                pick1 = Place.objects.filter(category=CHOICE_CATEGORY[choice_no-1][1])[0:3]
                pick2 = Place.objects.filter(category=CHOICE_CATEGORY[choice_no-2][1])[0:3]
                pick3 = Place.objects.filter(category=CHOICE_CATEGORY[choice_no-3][1])[0:3]
                pick = (pick1|pick2|pick3)
                
                serializer = PlaceSelectSerializer(pick, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                place_list = []
                pick = Place.objects.filter(category=CHOICE_CATEGORY[choice_no-1][1])[0:12]
                serializer = PlaceSelectSerializer(pick, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


##### 장소(리뷰가 없거나, 비로그인 계정일 경우) #####
class NewUserPlaceListView(APIView):
    permission_classes = [AllowAny]

    #맛집 전체 리스트
    @swagger_auto_schema(operation_summary="맛집 전체 리스트",
                    responses={200 : '성공', 500 : '서버 에러'})
    #맛집 리스트 추천
    def get(self, request, place_id, category):
        place_list = rcm_place_new_user(place_id=place_id, category=str(category))
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(place_list)])
        place = Place.objects.filter(id__in=place_list).order_by(preserved)
        serializer = PlaceSerializer(place, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

##### 장소 #####
class UserPlaceListView(APIView):
    permission_classes = [AllowAny]

    #맛집 전체 리스트
    @swagger_auto_schema(operation_summary="맛집 전체 리스트",
                    responses={200 : '성공', 500 : '서버 에러'})
    #맛집 리스트 추천
    def get(self, request, cate_id):
        # 지역 선택일 경우
        place_list = rcm_place_user(user_id = request.user.id, cate_id=cate_id)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(place_list)])
        place = Place.objects.filter(id__in=place_list).order_by(preserved)
        serializer = PlaceSerializer(place, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    #맛집 삭제
    @swagger_auto_schema(operation_summary="맛집 삭제",
                    responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def delete(self, request, place_id):
        place = get_object_or_404(Place, id=place_id)
        place.delete()
        return Response({"message":"맛집 삭제 완료"},status=status.HTTP_200_OK)

class PlaceBookmarkView(APIView):
    permission_classes = [IsAuthenticated] 

    #맛집 북마크
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

#####검색#####
class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **wsargs):
        query = request.GET.get('keyword')
        if not query:
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        results = client.perform_search(query)
        return Response(results)
