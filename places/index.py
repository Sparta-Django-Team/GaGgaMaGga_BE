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
        'searchableAttributes' : ["plaece_name", "catergory", "rating", "palce_address", "place_number"]
    }
