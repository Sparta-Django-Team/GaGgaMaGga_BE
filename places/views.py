from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

from .models import Place

# 장소 북마크
class AddBookmarkView(APIView):
    permissions_classes = [IsAuthenticated] 
    
    def post(self, request, place_id):
        place = get_object_or_404(Place, id=place_id)
        if request.user in place.place_bookmark.all():
            place.place_bookmark.remove(request.user)
            return Response("북마크취소했습니다.", status=status.HTTP_204_NO_CONTENT)
        else:
            place.place_bookmark.add(request.user)
            return Response("북마크했습니다.", status=status.HTTP_200_OK)