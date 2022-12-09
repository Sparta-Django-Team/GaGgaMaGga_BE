# Generated by Django 4.1.3 on 2022-12-09 02:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggedin',
            name='update_ip',
            field=models.GenericIPAddressField(null=True, validators=[django.core.validators.validate_ipv46_address], verbose_name='로그인한 IP'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics', validators=[django.core.validators.validate_image_file_extension], verbose_name='프로필 사진'),
        ),
    ]