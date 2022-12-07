from django.urls import path

from . import views

urlpatterns = [
    #Place
    path('', views.UserPlaceListView.as_view(), name='user_place_list_view'),
    path('new/<int:place_id>/<str:category>/', views.NewUserPlaceListView.as_view(), name='new_user_place_list_view'),
    path('<int:place_id>/', views.PlaceDetailView.as_view(), name='place_detail_view'),
    path('<int:place_id>/bookmarks/',views.PlaceBookmarkView.as_view(), name='place_bookmark_view'),
    
    #Recommendation
    path('new/<int:cate_id>/', views.NewUserPlaceListView.as_view(), name='new_user_place_list_view'),
    path('selection/<int:choice_no>/', views.PlaceSelectView.as_view(), name="place_select_view"),
    
    #Search
    path('search/', views.SearchListView.as_view(), name='search'),
]