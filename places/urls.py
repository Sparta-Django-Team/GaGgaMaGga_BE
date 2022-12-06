from django.urls import path

from . import views

urlpatterns = [
    path('<int:place_id>/bookmarks/',views.PlaceBookmarkView.as_view(), name='place_bookmark_view'),
    path('search/', views.SearchListView.as_view(), name='search'),
]