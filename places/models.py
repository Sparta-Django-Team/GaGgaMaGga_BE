from django.db import models

from users.models import User
# Create your models here.

class Place(models.Model):
    place_name = models.CharField('장소명',max_length=50)
    category = models.CharField('카테고리',default="",max_length=20)
    rating = models.DecimalField('별점', max_digits=3, decimal_places=2, default=0)
    place_address = models.CharField('주소', max_length=100)
    place_number = models.IntegerField('장소 전화번호')
    place_time = models.DateField('영업 시간',blank=True, default="")
    place_img = models.TextField('장소 이미지')
    latitude = models.FloatField('위도', null=True, blank=True)
    longitude = models.FloatField('경도', null=True, blank=True)
    munu = models.CharField('메뉴',null=True, blank=True, max_length=255)

    place_bookmark = models.ManyToManyField(User, verbose_name='장소 북마크', related_name="bookmark_place",blank=True)

    class Meta:
        db_table = 'places'

    def __str__(self):
        return f'[장소명]{self.place_name}'