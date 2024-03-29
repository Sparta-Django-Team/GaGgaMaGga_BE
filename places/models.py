from django.db import models
from django.db.models import Q
from django.core.validators import MaxValueValidator

from users.models import User


class PlaceQerySet(models.QuerySet):
    def search(self, query):
        lookup = (Q(place_name__contains=query)| Q(category__contains=query)
        | Q(place_address__contains=query)| Q(place_number__contains=query))
        qs = self.filter(lookup)
        return qs


class PlaceManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PlaceQerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query)


class Place(models.Model):
    place_name = models.CharField("장소명", max_length=50)
    category = models.CharField("카테고리", max_length=20)
    rating = models.DecimalField("별점", max_digits=3, decimal_places=2, default=0, validators=[MaxValueValidator(5)])
    menu = models.TextField("메뉴", null=True)
    place_desc = models.CharField("소개글", max_length=255, null=True)
    place_address = models.CharField("주소", max_length=100)
    place_number = models.CharField("장소 전화번호", max_length=20)
    place_time = models.CharField("영업 시간", max_length=30)
    place_img = models.TextField("장소 이미지", null=True)
    latitude = models.CharField("위도", max_length=50, null=True)
    longitude = models.CharField("경도", max_length=50, null=True)
    hit = models.PositiveIntegerField("조회수", default=0)

    place_bookmark = models.ManyToManyField(User, verbose_name="장소 북마크", related_name="bookmark_place", blank=True)

    objects = PlaceManager()

    class Meta:
        db_table = "places"

    def __str__(self):
        return f"[장소명]{self.place_name}"

    @property
    def hit_count(self):
        self.hit += 1
        self.save()