from django.db import models

from users.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, verbose_name='작성자', on_delete=models.CASCADE)
    content = models.CharField('내용', max_length=30)
    created_at = models.DateTimeField('생성 시간', auto_now_add=True)
    is_seen = models.BooleanField('읽음 처리', default=False)
