from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from notification.models import Notification
from .serializers import NotificationSerializer, NotificationDetailSerializer




class NotificationView(APIView):
    def get(self, request, user_id):
        notifiactions = Notification.objects.filter(Q(user_id=user_id) & Q(is_seen=False))
        serializer = NotificationSerializer(notifiactions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class NotificationDetailView(APIView) :
    def put(self, request, notification_id) :
        notification = get_object_or_404(Notification, id=notification_id)
        if request.user == notification.user :
            serializer = NotificationDetailSerializer(notification, data=request.data, partial=True)
            if serializer.is_valid() :
                serializer.save(is_seen=True)
                return Response({"message": "읽음 처리 완료"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)
            
    
# def put(self, request, place_id, review_id):
# review = get_object_or_404(Review, id=review_id)
# if request.user == review.author:
#     serializer = ReviewCreateSerializer(review, data=request.data, partial=True, context={"place_id":place_id, "review_id":review_id, "request":request})
#     if serializer.is_valid():
#         serializer.save(author=request.user, review_id=review_id)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)