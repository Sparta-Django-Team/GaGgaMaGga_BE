from django.urls import path

from . import views

urlpatterns = [
    # Review
    path('<int:place_id>/', views.ReviewListView.as_view(), name='review_list_view'),
    path('details/<int:place_id>/<int:review_id>/',views.ReviewDetailView.as_view(), name='review_detail_view'),
    path('<int:review_id>/likes/',views.ReviewLikeView.as_view(), name='review_like_view'),
    path('review-rank/',views.ReviewRankView.as_view(), name='reveiw_rank_view'),

    # Comment
    path('<int:review_id>/comments/',views.CommentListView.as_view(), name='comment_list_view'),
    path('<int:review_id>/comments/<int:comment_id>/',views.CommentDetailView.as_view(), name='comment_detail_view'),
    path('comments/<int:comment_id>/likes/',views.CommentLikeView.as_view(), name='comment_like_view'),

    # Recomment
    path('<int:review_id>/comments/<int:comment_id>/recomments/',views.RecommentListView.as_view(), name='recomment_list_view'),
    path('<int:review_id>/comments/<int:comment_id>/recomments/<int:recomment_id>/',views.RecommentDetailView.as_view(), name='recomment_detail_view'),
    path('recomments/<int:recomment_id>/likes/',views.RecommentLikeView.as_view(), name='recomment_like_view'),
]

