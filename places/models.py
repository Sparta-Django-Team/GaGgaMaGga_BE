from django.db import models

# Create your models here.

class Place(models.Model):
    place_name = models.CharField('장소명',max_length=50)
    common_address = models.CharField('구', max_length=100)
    place_address = models.CharField('주소', max_length=100)
    place_breaktime = models.DateField('브레이크타임',blank=True)
    place_category = models.CharField('카테고리',max_length=50)
    place_number = models.IntegerField('장소 전화번호')
    rating_sum = models.IntegerField('별점합')
    rating_cnt = models.ImageField('별점개수')
    place_img = models.TextField('장소이미지')
    latitude = models.FloatField('위도')
    longitude = models.FloatField('경도')


    class Meta:
        db_table = 'places'

    def __str__(self):
        return f'[지역]{self.common_address} [장소명]{self.place_name}'