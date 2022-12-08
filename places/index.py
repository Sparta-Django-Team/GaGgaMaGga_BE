from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Place

@register(Place)
class PlaceIndex(AlgoliaIndex):
    fields = [
        'place_name',
        'category',
        'rating',
        'place_address',
        'place_number',
        'place_img'
    ]

    settings = {
        'searchableAttributes' : ["place_name", "category", "palce_address", "place_number"]
    }
