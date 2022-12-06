from rest_framework import generics
from places. models import Place
from places.serializers import PlaceSerializer

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