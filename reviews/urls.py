from django.urls import path

from . import views

urlpatterns = [
    path('<int:place_id>/review/', views.ReviewLoadView.as_view(), name='review_load_view'),
    path('<int:place_id>/', views.ReviewCreateView.as_view(), name='review_create_view'),
    path('<int:review_id>/reviewdetail/',views.ReviewDetailView.as_view(), name='review_detail_view'),
    path('<int:review_id>/reviewupdate/',views.ReviewDetailView.as_view(), name='review_update_view'),
    path('<int:review_id>/comments/',views.CommentView.as_view(), name='comment_view'),
    path('<int:review_id>/comments/<int:comment_id>/',views.CommentDetailView.as_view(), name='comment_edit_view'),
]

