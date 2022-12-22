import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

import sys
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaggamagga.settings')
django.setup()

# 유사한 유저 정보 조회 및 추천(기존 사용이력이 없는 사용자)
def rcm_place_new_user(review_user, place_id):

    # 유저 데이터 데이터 프레임 생성
    new_idx = int(review_user.iloc[len(review_user)-1].name)+1
    review_user.loc[new_idx] = np.nan
    review_user.loc[new_idx, place_id] = 5
    review_user = review_user.fillna(0)

    # 코사인 유사도 분석
    user_sim_np = cosine_similarity(review_user, review_user)
    user_sim_df = pd.DataFrame(user_sim_np, index=review_user.index, columns=review_user.index)

    # 유사한 유저 선택
    picked_user = user_sim_df.sort_values(by=new_idx, ascending=False).index[1]
    result = review_user.query(f"author_id == {picked_user}").sort_values(ascending=False, by=picked_user, axis=1)

    # 가장 유사한 유저 추천
    result_list = []
    for column in result:
        result_list.append(column)
    return result_list


# 유사한 유저 정보 조회 및 추천(기존 유저)
def rcm_place_user(review_user, user_id):

    # 코사인 유사도 분석
    user_sim_np = cosine_similarity(review_user, review_user)
    user_sim_df = pd.DataFrame(user_sim_np, index=review_user.index, columns=review_user.index)

    # 유사한 유저 선택
    picked_user = user_sim_df.sort_values(by=user_id, ascending=False).index[1]
    result = review_user.query(f"author_id == {picked_user}").sort_values(ascending=False, by=picked_user, axis=1)

    # 가장 유사한 유저 추천
    result_list = []
    for column in result:
        result_list.append(column)
    return result_list