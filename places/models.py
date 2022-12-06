from django.db import models

from users.models import User

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
    # menu = models.CharField('메뉴',null=True, blank=True, max_length=200)
    score_taste = models.IntegerField('맛',null=True, blank=True)
    score_service = models.IntegerField('서비스',null=True, blank=True)
    score_cleanliness = models.IntegerField('청결도',null=True, blank=True)
    hit = models.PositiveIntegerField('조회수', default=0)

    place_bookmark = models.ManyToManyField(User, verbose_name='장소 북마크', related_name="bookmark_place",blank=True)

    class Meta:
        db_table = 'places'

    def __str__(self):
        return f'[장소명]{self.place_name}'

    @property
    def hit_count(self):
        self.hit +=1
        self.save()