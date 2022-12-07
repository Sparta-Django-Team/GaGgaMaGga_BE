import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

import json

import sys
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaggamagga.settings')
django.setup()

from reviews.models import Review
from places.models import Place

CHOICE_ONE = ['분식', '한식', '돼지고기구이','치킨,닭강정', '햄버거', '피자', '중식당', '일식당', '양식',  '태국음식', '인도음식', '베트남음식', '제주시', '서귀포시']

# 유사한 유저 정보 조회 및 추천(기존 사용이력이 없는 사용자)
def rcm_place_new_user(place_id, category):
    places = pd.DataFrame(list(Place.objects.values()))
    cate_id = CHOICE_ONE.index(category)
    print(cate_id)
    if cate_id <= 12:       # 카테고리일 경우
        places = places[places['category'].str.contains(category)]
    else:       # 장소일 경우
        places = places[places['place_address'].str.contains(category)]
    reviews = pd.DataFrame(list(Review.objects.values()))
    places.rename(columns={'id':'place_id'}, inplace=True)


    place_ratings = pd.merge(places, reviews, on='place_id')
    
    review_user = place_ratings.pivot_table('rating_cnt', index='author_id', columns='place_id')
    print("----------------")
    print(review_user)

    review_user.loc[len(review_user)+1] = np.nan
    review_user = review_user.fillna(0)
    review_user.loc[len(review_user), place_id] = 5
    print(review_user)

    user_sim_np = cosine_similarity(review_user, review_user)
    user_sim_df = pd.DataFrame(user_sim_np, index=review_user.index, columns=review_user.index)
    print(user_sim_df.head)
    print(user_sim_df[len(review_user)].sort_values(ascending=False)[:])

    picked_user = user_sim_df[len(review_user)].sort_values(ascending=False)[:].index[1]
    result = review_user.query(f"author_id == {picked_user}").sort_values(ascending=False, by=picked_user, axis=1)

    result_list = []
    for column in result:
        result_list.append(column)
    return result_list


# 유사한 유저 정보 조회 및 추천(기존 유저)
def rcm_place_user(user_id):
    places = pd.DataFrame(list(Place.objects.values()))
    if 0:       # 카테고리일 경우
        places = places[places['category'].str.contains("분식")]
    else:       # 장소일 경우
        places = places[places['place_address'].str.contains("압구정")]

    reviews = pd.DataFrame(list(Review.objects.values()))
    places.rename(columns={'id':'place_id'}, inplace=True)

    place_ratings = pd.merge(places, reviews, on='place_id')
    review_user = place_ratings.pivot_table('rating_cnt', index='author_id', columns='place_id')
    review_user = review_user.fillna(0)

    user_sim_np = cosine_similarity(review_user, review_user)
    user_sim_df = pd.DataFrame(user_sim_np, index=review_user.index, columns=review_user.index)
    print(user_sim_df.head)
    print(user_sim_df[user_id].sort_values(ascending=False)[:])

    picked_user = user_sim_df[user_id].sort_values(ascending=False)[:].index[1]
    print(picked_user)
    result = review_user.query(f"author_id == {picked_user}").sort_values(ascending=False, by=picked_user, axis=1)

    result_list = []
    for column in result:
        result_list.append(column)
    print(result_list)
    return result_list
