from django.urls import path

from . import views

urlpatterns = [
    path('<int:place_id>/bookmark/',views.AddBookmarkView.as_view(), name='add_bookmark_view'),
]