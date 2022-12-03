from django.db import models

# Create your models here.

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
    munu = models.CharField('메뉴',null=True, blank=True, max_length=200)


    class Meta:
        db_table = 'places'

    def __str__(self):
        return f'[지역]{self.common_address} [장소명]{self.place_name}'