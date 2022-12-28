from django.urls import path

from . import views

urlpatterns = [
    # Notification
    path("<int:user_id>/", views.NotificationView.as_view(), name="notification"),
    path("alarm/<int:notification_id>/", views.NotificationDetailView.as_view(), name="notification_detail"),
]
