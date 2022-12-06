from django.db import models
from users.models import User
from django.db .models import Q


class PlaceQerySet(models.QuerySet) :
    def search(self, query) :
        lookup = Q(place_name__contains=query) | Q(category__contains=query) | Q(place_address__contains=query) | Q(place_number__contains=query)
        qs = self.filter(lookup)
        return qs

class PlaceManager(models.Manager) :
    def get_queryset(self, *args, **kwargs) :
        return PlaceQerySet(self.model, using=self._db)

    def search(self, query, user=None) :
        return self.get_queryset().search(query)

class Place(models.Model):
    place_name = models.CharField('장소명',max_length=50)
    category = models.CharField('카테고리', max_length=20)
    rating = models.DecimalField('별점', max_digits=3, decimal_places=2, default=0)
    place_address = models.CharField('주소', max_length=100)
    place_number = models.CharField('장소 전화번호', max_length=20)
    place_time = models.CharField('영업 시간',max_length=30)
    place_img = models.TextField('장소 이미지')
    latitude = models.IntegerField('위도',null=True, blank=True)
    longitude = models.IntegerField('경도',null=True, blank=True)
    menu = models.CharField('메뉴',null=True, blank=True, max_length=200)

    place_bookmark = models.ManyToManyField(User, verbose_name='장소 북마크', related_name="bookmark_place",blank=True)
    
    objects = PlaceManager()

    class Meta:
        db_table = 'places'

    def __str__(self):
        return f'[장소명]{self.place_name}'