# Generated by Django 4.1.3 on 2022-12-05 23:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('places', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=100, verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
                ('comment_like', models.ManyToManyField(blank=True, related_name='like_comment', to=settings.AUTH_USER_MODEL, verbose_name='댓글 좋아요')),
            ],
            options={
                'db_table': 'review_comment',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Recomment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=100, verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_recomments', to='reviews.comment', verbose_name='댓글')),
                ('recomment_like', models.ManyToManyField(blank=True, related_name='like_recomment', to=settings.AUTH_USER_MODEL, verbose_name='대댓글 좋아요')),
            ],
            options={
                'db_table': 'review_recomment',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500, verbose_name='내용')),
                ('review_image_one', models.ImageField(blank=True, upload_to='review_pics', verbose_name='이미지 1')),
                ('review_image_two', models.ImageField(blank=True, upload_to='review_pics', verbose_name='이미지 2')),
                ('review_image_three', models.ImageField(blank=True, upload_to='review_pics', verbose_name='이미지 3')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='후기 생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='후기 수정 시간')),
                ('rating_cnt', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='별점')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.place', verbose_name='장소')),
                ('review_like', models.ManyToManyField(blank=True, related_name='like_review', to=settings.AUTH_USER_MODEL, verbose_name='후기 좋아요')),
            ],
            options={
                'db_table': 'review',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('욕설이 들어갔어요.', '욕설이 들어갔어요.'), ('성적인 발언이 들어갔어요', '성적인 발언이 들어갔어요.'), ('정치적 요소가 들어갔어요', '정치적 요소가 들어갔어요.'), ('관계 없는 내용이예요.', '관계 없는 내용이예요.'), ('도배된 내용이예요.', '도배된 내용이예요.'), ('광고성이 포함된 글이예요', '광고성이 포함된 글이예요'), ('기타', '기타')], max_length=30, verbose_name='신고 카테고리')),
                ('content', models.TextField(blank=True, max_length=500, verbose_name='신고 내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.comment', verbose_name='댓글')),
                ('recomment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.recomment', verbose_name='대댓글')),
                ('review', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.review', verbose_name='후기')),
            ],
            options={
                'db_table': 'reports',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_comments', to='reviews.review', verbose_name='후기'),
        ),
    ]
