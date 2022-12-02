from django.db import models

# Create your models here.
class Place(models.Model):
    class Meta():
        db_table = 'db_place'

    place_name = models.CharField(max_length=50)
    common_address = models.CharField(max_length=100)
    place_address = models.CharField(max_length=100)
    place_breaktime = models.DateTimeField()
    place_category = models.CharField(max_length=50)
    place_number = models.IntegerField()
    rating_sum = models.IntegerField()
    rating_cnt = models.IntegerField()
    place_img = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()