from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from django.db.models import Case, When

from drf_yasg.utils import swagger_auto_schema

from gaggamagga.permissions import IsAdminOrOntherReadOnly
from gaggamagga.pagination import PaginationHandlerMixin
from . import client
from .models import Place
from reviews.models import Review
from .serializers import PlaceSerializer
from .rcm_places import rcm_place_user, rcm_place_new_user

import random
import pandas as pd
import numpy as np

CHOICE_CATEGORY = [
    "분식",
    "한식",
    "돼지고기구이",
    "치킨,닭강정",
    "햄버거",
    "피자",
    "중식",
    "일식",
    "양식",
    "태국음식",
    "인도음식",
    "베트남음식",
    "제주시",
    "서귀포시",
]



class PlaceListPagination(PageNumberPagination):
    page_size = 10

##### 맛집 #####
class PlaceDetailView(APIView):
    permission_classes = [IsAdminOrOntherReadOnly]

    # 맛집 상세 페이지
    @swagger_auto_schema(
        operation_summary="맛집 상세 페이지",
        responses={200: "성공", 404: "찾을 수 없음", 500: "서버 에러"},
    )
    def get(self, request, place_id):
        place = get_object_or_404(Place, id=place_id)
        place.hit_count
        serializer = PlaceSerializer(place)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 맛집 삭제
    @swagger_auto_schema(
        operation_summary="맛집 삭제",
        responses={200: "성공", 401: "인증 에러", 404: "찾을 수 없음", 500: "서버 에러"},
    )
    def delete(self, request, place_id):
        place = get_object_or_404(Place, id=place_id)
        place.delete()
        return Response({"message": "맛집 삭제 완료"}, status=status.HTTP_200_OK)

class PlaceBookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    # 맛집 북마크
    @swagger_auto_schema(
        operation_summary="맛집 북마크",
        responses={200: "성공", 401: "인증 에러", 404: "찾을 수 없음", 500: "서버 에러"},
    )
    def post(self, request, place_id):
        place = get_object_or_404(Place, id=place_id)
        if request.user in place.place_bookmark.all():
            place.place_bookmark.remove(request.user)
            return Response({"message": "북마크를 취소했습니다."}, status=status.HTTP_200_OK)
        else:
            place.place_bookmark.add(request.user)
            return Response({"message": "북마크를 했습니다."}, status=status.HTTP_200_OK)

##### 취향 선택 #####
class PlaceSelectView(APIView):
    permission_classes = [AllowAny]

    # 맛집 취향 선택(리뷰가 없거나, 비로그인 계정일 경우)
    @swagger_auto_schema(
        operation_summary="맛집 취향 선택", responses={200: "성공", 500: "서버 에러"}
    )
    def get(self, request, choice_no):
        place_list = []
        load_no = random.randint(1, 6) 

        # Case1: 장소(제주시, 서귀포시)를 선택했을 경우
        if choice_no > 12:
            place_list = []

            # 해당 장소의 음식 종류별 맛집 하나씩 호출하고 place_list에 담는다.
            for i in range(0, 12):
                pick = Place.objects.filter(place_address__contains=CHOICE_CATEGORY[choice_no - 1],category=CHOICE_CATEGORY[i]).first()

                if pick != None:    # pick이 선택되었을 경우
                    place_list.append(pick.id)
                else:               # pick이 선택되지 않았을 경우
                    pass

            # for문에서 생성된 리스트에 해당하는 데이터 생성 후 json 전달
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(place_list)])
            place = Place.objects.filter(id__in=place_list).order_by(preserved)
            serializer = PlaceSerializer(place, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Case2: 음식(한식, 분식, 양식 등)을 선택했을 경우
        else:

            # 한식, 패스트푸드, 아시아 선택햇을 경우
            if (choice_no == 3) | (choice_no == 6) | (choice_no == 12):
                place_list = []

                # 각 카테고리에 해당하는 맛집 3개씩 호출
                pick1 = Place.objects.filter(category=CHOICE_CATEGORY[choice_no - 1])[load_no - 1 : load_no + 2]
                pick2 = Place.objects.filter(category=CHOICE_CATEGORY[choice_no - 2])[load_no - 1 : load_no + 2]
                pick3 = Place.objects.filter(category=CHOICE_CATEGORY[choice_no - 3])[load_no - 1 : load_no + 2]

                # 호출한 맛집 리스트 병합 후 json 전달
                pick = pick1 | pick2 | pick3
                serializer = PlaceSerializer(pick, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # 한식, 패스트푸드, 아시아 외의 카테고리를 선택했을 경우
            else:
                place_list = []

                # 카테고리에 해당하는 맛집 9개 호출 후 json 전달
                pick = Place.objects.filter(category=CHOICE_CATEGORY[choice_no - 1])[0:9]
                serializer = PlaceSerializer(pick, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


##### 맛집(리뷰가 없거나, 비로그인 계정일 경우) #####
class NewUserPlaceListView(PaginationHandlerMixin, APIView):
    permission_classes = [AllowAny]
    pagination_class = PlaceListPagination

    # 맛집 리스트 추천
    @swagger_auto_schema(
        operation_summary="맛집 리스트 추천(비유저)", responses={200: "성공", 500: "서버 에러"}
    )
    def get(self, request, place_id, category):
        places = pd.DataFrame(list(Place.objects.values()))     # DB에서 가져온 맛집 정보 데이터프레임 생성
        cate_id = CHOICE_CATEGORY.index(category) + 1           # 전달받은 카테고리의 인덱스 저장

        if cate_id <= 12:  # Case1: 음식(한식, 분식, 양식 등)을 선택했을 경우

            # 한식, 패스트푸드, 아시아 선택햇을 경우
            if (cate_id == 3) | (cate_id == 6) | (cate_id == 12):

                # 인덱스를 통해 각 카테고리 이름 저장
                category1 = CHOICE_CATEGORY[cate_id - 1]
                category2 = CHOICE_CATEGORY[cate_id - 2]
                category3 = CHOICE_CATEGORY[cate_id - 3]

                # 각 카테고리에 해당하는 맛집 정보를 Dataframe에서 가져와서 저장
                place1 = places[places["category"].str.contains(category1)]
                place2 = places[places["category"].str.contains(category2)]
                place3 = places[places["category"].str.contains(category3)]

                # 각 카테고리별 리스트를 만든 후, 저장된 데이터프레임 병합
                place_list = [place1, place2, place3]
                places = pd.concat(place_list, ignore_index=True)

            # 한식, 패스트푸드, 아시아 외의 카테고리를 선택했을 경우
            else:
                cate = CHOICE_CATEGORY[cate_id - 1]
                places = places[places["category"].str.contains(cate)]

        else:  # Case2: 장소(제주시, 서귀포시)를 선택했을 경우
            cate = CHOICE_CATEGORY[cate_id - 1]
            places = places[places["place_address"].str.contains(cate)]


        # 리뷰 데이터프레임 호출
        reviews = pd.DataFrame(list(Review.objects.values()))

        # 맛집(place) 데이터프레임과 리뷰 데이터프레임 병합
        places.rename(columns={"id": "place_id"}, inplace=True)
        place_ratings = pd.merge(places, reviews, on="place_id")

        # 병합된 데이터프레임에서 장소, 리뷰유저를 기준, 별점을 값으로 피봇테이블 생성
        review_user = place_ratings.pivot_table("rating_cnt", index="author_id", columns="place_id")

        # 추천 머신러닝 실행
        place_list = rcm_place_new_user(review_user=review_user, place_id=place_id)

        # 머신러닝 결과 순서 리스트에 저장 후 순서대로 쿼리셋 호출
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(place_list)])
        place = Place.objects.filter(id__in=place_list).order_by(preserved)

        # 페이지네이션으로 구분하여 json 전달
        page = self.paginate_queryset(place)
        serializer = self.get_paginated_response(PlaceSerializer(page, many=True).data)
        return Response(serializer.data, status=status.HTTP_200_OK)


##### 맛집(유저일 경우) #####
class UserPlaceListView(PaginationHandlerMixin, APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PlaceListPagination

    # 맛집 리스트 추천
    @swagger_auto_schema(
        operation_summary="맛집 리스트 추천(유저)",
        responses={200: "성공", 401: "인증 에러", 500: "서버 에러"},
    )
    def get(self, request, cate_id):
        places = pd.DataFrame(list(Place.objects.values()))     # DB에서 가져온 맛집 정보 데이터프레임 생성

        if cate_id <= 12:  # Case1: 음식(한식, 분식, 양식 등)을 선택했을 경우
            
            # 한식, 패스트푸드, 아시아 선택햇을 경우
            if (cate_id == 3) | (cate_id == 6) | (cate_id == 12):

                # 인덱스를 통해 각 카테고리 이름 저장
                category1 = CHOICE_CATEGORY[cate_id - 1]
                category2 = CHOICE_CATEGORY[cate_id - 2]
                category3 = CHOICE_CATEGORY[cate_id - 3]

                # 각 카테고리에 해당하는 맛집 정보를 Dataframe에서 가져와서 저장
                place1 = places[places["category"].str.contains(category1)]
                place2 = places[places["category"].str.contains(category2)]
                place3 = places[places["category"].str.contains(category3)]

                # 각 카테고리별 리스트를 만든 후, 저장된 데이터프레임 병합
                place_list = [place1, place2, place3]
                places = pd.concat(place_list, ignore_index=True)

            # 한식, 패스트푸드, 아시아 외의 카테고리를 선택했을 경우
            else:
                category = CHOICE_CATEGORY[cate_id - 1]
                places = places[places["category"].str.contains(category)]

        else:  # Case2: 장소(제주시, 서귀포시)를 선택했을 경우
            category = CHOICE_CATEGORY[cate_id - 1]
            places = places[places["place_address"].str.contains(category)]

        # 리뷰 데이터프레임 호출
        reviews = pd.DataFrame(list(Review.objects.values()))

        # 맛집(place) 데이터프레임과 리뷰 데이터프레임 병합
        places.rename(columns={"id": "place_id"}, inplace=True)
        place_ratings = pd.merge(places, reviews, on="place_id")

        # 병합된 데이터프레임에서 장소, 리뷰유저를 기준, 별점을 값으로 피봇테이블 생성
        review_user = place_ratings.pivot_table("rating_cnt", index="author_id", columns="place_id")

        # 선택한 카테고리에 해당하는 리뷰를 작성하지 않은 유저일 경우 선택된 카테고리를 기반으로 임시 경험데이터 생성
        if request.user.id not in review_user.index:
            col = random.choice(review_user.columns.to_list())
            review_user.loc[request.user.id] = np.nan
            review_user.loc[request.user.id, col] = 5
        review_user = review_user.fillna(0)

        # 추천 머신러닝 실행
        place_list = rcm_place_user(review_user=review_user, user_id=request.user.id)

        # 머신러닝 결과 순서 리스트에 저장 후 순서대로 쿼리셋 호출
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(place_list)])
        place = Place.objects.filter(id__in=place_list).order_by(preserved)

        # 페이지네이션으로 구분하여 json 전달
        page = self.paginate_queryset(place)
        serializer = self.get_paginated_response(PlaceSerializer(page, many=True).data)
        return Response(serializer.data, status=status.HTTP_200_OK)

##### 검색 #####
class SearchListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="검색", responses={200: "성공", 400: "쿼리 에러", 500: "서버 에러"}
    )
    def get(self, request):
        query = request.GET.get("keyword")
        if query == "":
            return Response({"message": "공백은 입력 불가"}, status=status.HTTP_400_BAD_REQUEST)
        if not query:
            return Response({"message": "쿼리 아님"}, status=status.HTTP_400_BAD_REQUEST)
        results = client.perform_search(query)
        return Response(results, status=status.HTTP_200_OK)