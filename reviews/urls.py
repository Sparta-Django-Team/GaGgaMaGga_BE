from django.urls import path

from . import views

urlpatterns = [
    path('<int:place_id>/review/', views.ReviewView.as_view(), name='review_view'),
    path('<int:place_id>/', views.ReviewView.as_view(), name='review_create_view'),
]