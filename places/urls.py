from django.urls import path

from . import views

urlpatterns = [
    #Place
    path('', views.PlaceListView.as_view(), name='place_list_view'),
    path('<int:place_id>/', views.PlaceDetailView.as_view(), name='place_detail_view'),
    path('<int:place_id>/bookmarks/',views.PlaceBookmarkView.as_view(), name='place_bookmark_view'),

    #Recommend
    path('recommendation/',views.RecommendPlaceView.as_view(), name='recommend_place_view'),
]