from django.urls import path

from . import views

urlpatterns = [
    # Review
    path('<int:place_id>/review/', views.ReviewLoadView.as_view(), name='review_load_view'),
    path('<int:place_id>/', views.ReviewCreateView.as_view(), name='review_create_view'),
    path('<int:review_id>/reviewdetail/',views.ReviewDetailView.as_view(), name='review_detail_view'),
    path('<int:review_id>/reviewupdate/',views.ReviewDetailView.as_view(), name='review_update_view'),
    path('<int:review_id>/like/',views.ReviewLikeView.as_view(), name='review_like_view'),
    # Comment
    path('<int:review_id>/comments/',views.CommentView.as_view(), name='comment_view'),
    path('<int:review_id>/comments/<int:comment_id>/',views.CommentDetailView.as_view(), name='comment_edit_view'),
    path('comments/<int:comment_id>/like/',views.CommentLikeView.as_view(), name='comment_like_view'),
    # Recomment
    path('<int:review_id>/<int:comment_id>/recomments/',views.RecommentView.as_view(), name='recomment_view'),
    path('<int:review_id>/<int:comment_id>/recomments/<int:recomment_id>/',views.RecommentDetailView.as_view(), name='recomment_detail_view'),

]

