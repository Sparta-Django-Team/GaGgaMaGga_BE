from django.urls import path

from . import views

urlpatterns = [
    #Place
    path('', views.PlaceListView.as_view(), name='place_list_view'),
    path('<int:place_id>/', views.PlaceDetailView.as_view(), name='place_detail_view'),
    path('<int:place_id>/bookmarks/',views.PlaceBookmarkView.as_view(), name='place_bookmark_view'),
    path('search/', views.SearchListView.as_view(), name='search'),
]