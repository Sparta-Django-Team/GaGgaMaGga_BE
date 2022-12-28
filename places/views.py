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

CHOICE_ONE = [
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

CHOICE_CATEGORY = (
    ("1", "분식"),
    ("2", "한식"),
    ("3", "돼지고기구이"),
    ("4", "치킨,닭강정"),
    ("5", "햄버거"),
    ("6", "피자"),
    ("7", "중식"),
    ("8", "일식"),
    ("9", "양식"),
    ("10", "태국음식"),
    ("11", "인도음식"),
    ("12", "베트남음식"),
    ("13", "제주시"),
    ("14", "서귀포시"),
)


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
        # Case1: choice place location
        if choice_no > 12:
            place_list = []
            for i in range(0, 12):
                pick = Place.objects.filter(place_address__contains=CHOICE_CATEGORY[choice_no - 1][1],category=CHOICE_CATEGORY[i][1],).first()
                if pick == None:
                    pass
                else:
                    place_list.append(pick.id)

            # Create list for custom sorting
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(place_list)])
            place = Place.objects.filter(id__in=place_list).order_by(preserved)
            serializer = PlaceSerializer(place, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Case2: choice food group
        else:
            if (choice_no == 3) | (choice_no == 6) | (choice_no == 12):
                # Merge queryset for 3categories
                place_list = []
                pick1 = Place.objects.filter(category=CHOICE_CATEGORY[choice_no - 1][1])[load_no - 1 : load_no + 2]
                pick2 = Place.objects.filter(category=CHOICE_CATEGORY[choice_no - 2][1])[load_no - 1 : load_no + 2]
                pick3 = Place.objects.filter(category=CHOICE_CATEGORY[choice_no - 3][1])[load_no - 1 : load_no + 2]
                pick = pick1 | pick2 | pick3
                serializer = PlaceSerializer(pick, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                place_list = []
                pick = Place.objects.filter(category=CHOICE_CATEGORY[choice_no - 1][1])[0:9]
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
        places = pd.DataFrame(list(Place.objects.values()))
        cate_id = CHOICE_ONE.index(category) + 1
        if cate_id <= 12:  # Case1: choice food group
            if (cate_id == 3) | (cate_id == 6) | (cate_id == 12):
                category1 = CHOICE_CATEGORY[cate_id - 1][1]
                category2 = CHOICE_CATEGORY[cate_id - 2][1]
                category3 = CHOICE_CATEGORY[cate_id - 3][1]
                place1 = places[places["category"].str.contains(category1)]
                place2 = places[places["category"].str.contains(category2)]
                place3 = places[places["category"].str.contains(category3)]
                place_list = [place1, place2, place3]
                places = pd.concat(place_list, ignore_index=True)
            else:
                cate = CHOICE_CATEGORY[cate_id - 1][1]
                places = places[places["category"].str.contains(cate)]
        else:  # Case2: choice place location
            cate = CHOICE_CATEGORY[cate_id - 1][1]
            places = places[places["place_address"].str.contains(cate)]

        # Create dataframe
        reviews = pd.DataFrame(list(Review.objects.values()))

        places.rename(columns={"id": "place_id"}, inplace=True)
        place_ratings = pd.merge(places, reviews, on="place_id")
        review_user = place_ratings.pivot_table("rating_cnt", index="author_id", columns="place_id")
        place_list = rcm_place_new_user(review_user=review_user, place_id=place_id)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(place_list)])
        place = Place.objects.filter(id__in=place_list).order_by(preserved)
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
        places = pd.DataFrame(list(Place.objects.values()))
        if cate_id <= 12:  # Case1: choice food group
            if (cate_id == 3) | (cate_id == 6) | (cate_id == 12):
                category1 = CHOICE_CATEGORY[cate_id - 1][1]
                category2 = CHOICE_CATEGORY[cate_id - 2][1]
                category3 = CHOICE_CATEGORY[cate_id - 3][1]
                place1 = places[places["category"].str.contains(category1)]
                place2 = places[places["category"].str.contains(category2)]
                place3 = places[places["category"].str.contains(category3)]
                place_list = [place1, place2, place3]
                places = pd.concat(place_list, ignore_index=True)
            else:
                category = CHOICE_CATEGORY[cate_id - 1][1]
                places = places[places["category"].str.contains(category)]
        else:  # Case2: choice place location
            category = CHOICE_CATEGORY[cate_id - 1][1]
            places = places[places["place_address"].str.contains(category)]

        # Create dataframe
        reviews = pd.DataFrame(list(Review.objects.values()))
        places.rename(columns={"id": "place_id"}, inplace=True)
        place_ratings = pd.merge(places, reviews, on="place_id")
        review_user = place_ratings.pivot_table("rating_cnt", index="author_id", columns="place_id")

        if request.user.id not in review_user.index:
            col = random.choice(review_user.columns.to_list())
            review_user.loc[request.user.id] = np.nan
            review_user.loc[request.user.id, col] = 5
        review_user = review_user.fillna(0)
        place_list = rcm_place_user(review_user=review_user, user_id=request.user.id)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(place_list)])
        place = Place.objects.filter(id__in=place_list).order_by(preserved)
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