from django.db import models

from users.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='유저')
    content = models.CharField('내용', max_length=30)
