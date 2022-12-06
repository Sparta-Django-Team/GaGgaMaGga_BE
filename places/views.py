from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import generics
from places .models import Place
from places.serializers import PlaceSerializer

from drf_yasg.utils import swagger_auto_schema

##### 장소 #####
class PlaceBookmarkView(APIView):
    permissions_classes = [IsAuthenticated] 

    # 장소 북마크
    @swagger_auto_schema(operation_summary="장소 북마크",  
                responses={200 : '성공', 404 : '찾을 수 없음', 500 : '서버 에러'})
    def post(self, request, place_id):
        place = get_object_or_404(Place, id=place_id)
        if request.user in place.place_bookmark.all():
            place.place_bookmark.remove(request.user)
            return Response({"message":"북마크를 취소했습니다."}, status=status.HTTP_200_OK)
        else:
            place.place_bookmark.add(request.user)
            return Response({"message":"북마크를 했습니다."}, status=status.HTTP_200_OK)




class SearchListView(generics.ListAPIView) :
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_queryset(self, *args, **kwargs) :
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Place.objects.none()
        if q is not None:
            results = qs.search(q)
        return results