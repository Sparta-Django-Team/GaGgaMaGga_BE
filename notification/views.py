from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema

from .models import Notification
from .serializers import NotificationSerializer, NotificationDetailSerializer

class NotificationView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 읽지 않은 해당 알람 리스트
    @swagger_auto_schema(operation_summary="읽지 않은 해당 알람 리스트",  
                responses={200 : '성공', 500 : '서버 에러'})
    def get(self, request, user_id):
        notifiactions = Notification.objects.filter(Q(user_id=user_id) & Q(is_seen=False)).order_by('-created_at')
        serializer = NotificationSerializer(notifiactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NotificationDetailView(APIView) :
    permission_classes = [IsAuthenticated]
    
    # 알람 읽음 처리
    @swagger_auto_schema(operation_summary="알람 읽음 처리",  
                responses={200 : '성공', 400: '입력값 에러' , 403: '접근 권한 없음 ', 404 : '찾을 수 없음', 500 : '서버 에러'})  
    def put(self, request, notification_id) :
        notification = get_object_or_404(Notification, id=notification_id)
        print('hello')
        if request.user == notification.user :
            serializer = NotificationDetailSerializer(notification, data=request.data, partial=True)
            if serializer.is_valid() :
                serializer.save(is_seen=True)
                return Response({"message": "읽음 처리 완료"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)