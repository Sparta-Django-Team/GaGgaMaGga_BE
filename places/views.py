from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from .models import Place
from .serializers import PlaceLocationSelectSerializer

### Place Select ###
class PlaceLocationSelectView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        place = get_object_or_404(Place)
        serializer = PlaceLocationSelectSerializer(place, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

