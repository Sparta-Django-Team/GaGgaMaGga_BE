from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Place

@register(Place)
class PlaceIndex(AlgoliaIndex):
    fields = [ # aoglolia 페이지에서 확인할 필드 지정
        'place_name',
        'category',
        'rating',
        'place_address',
        'place_number',
        'place_img'
    ]

    settings = {           # 검색 가능한 필드 지정
        'searchableAttributes' : ["place_name", "category", "palce_address", "place_number"]
    }
