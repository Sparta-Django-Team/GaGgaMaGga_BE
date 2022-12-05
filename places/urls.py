from django.urls import path

from .views import PlaceLocationSelectView, RecommendPlaceView, PlaceDetailView

urlpatterns = [
    path('', PlaceLocationSelectView.as_view(), name="place_location"),
]
