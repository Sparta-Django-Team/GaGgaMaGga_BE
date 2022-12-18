# Generated by Django 4.1.3 on 2022-12-18 16:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 18, 16, 43, 56, 573922), verbose_name='계정 생성일'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_password_changed',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 18, 16, 43, 56, 573893), verbose_name='비밀번호 마지막 변경일'),
        ),
    ]