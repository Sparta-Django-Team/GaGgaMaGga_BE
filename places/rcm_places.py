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

def rcm_place(user_id):
    places = pd.DataFrame(list(Place.objects.values()))
    reviews = pd.DataFrame(list(Review.objects.values()))
    places.rename(columns={'id':'place_id'}, inplace=True)

    place_ratings = pd.merge(places, reviews, on='place_id')
    review_user = place_ratings.pivot_table('rating_cnt', index='author_id', columns='place_id')
    review_user = review_user.fillna(3)

    user_sim_np = cosine_similarity(review_user, review_user)
    user_sim_df = pd.DataFrame(user_sim_np, index=review_user.index, columns=review_user.index)
    print(user_sim_df.head)
    print(user_sim_df[user_id].sort_values(ascending=False)[:])

    picked_user = user_sim_df[user_id].sort_values(ascending=False)[:].index[1]

    result = review_user.query(f"author_id == {picked_user}").sort_values(ascending=False, by=picked_user, axis=1).transpose()[:50]
    print(result)
