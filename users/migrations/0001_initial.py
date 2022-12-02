from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': '이미 사용중인 아이디 이거나 탈퇴한 아이디입니다.'}, max_length=15, unique=True, verbose_name='아이디')),
                ('email', models.EmailField(error_messages={'unique': '이미 사용중인 이메일 이거나 탈퇴한 이메일입니다.'}, max_length=255, unique=True, verbose_name='이메일')),
                ('phone_number', models.CharField(blank=True, max_length=11, verbose_name='휴대폰 번호')),
                ('account_lock_count', models.IntegerField(default=0, verbose_name='로그인 제한 횟수')),
                ('account_lock_time', models.DateTimeField(null=True, verbose_name='로그인 제한 시간')),
                ('is_admin', models.BooleanField(default=False, verbose_name='관리자')),
                ('is_active', models.BooleanField(default=True, verbose_name='로그인 가능')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='이메일 확인')),
                ('withdraw', models.BooleanField(default=False, verbose_name='회원 비활성화')),
                ('password_expired', models.BooleanField(default=False, verbose_name='비밀번호 만료')),
                ('last_password_changed', models.DateTimeField(auto_now=True, verbose_name='비밀번호 마지막 변경일')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='계정 생성일')),
                ('withdraw_at', models.DateTimeField(null=True, verbose_name='계정 탈퇴일')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics', verbose_name='프로필 사진')),
                ('nickname', models.CharField(error_messages={'unique': '이미 사용중인 닉네임 이거나 탈퇴한 닉네임입니다.'}, max_length=10, null=True, unique=True, verbose_name='닉네임')),
                ('intro', models.CharField(max_length=100, null=True, verbose_name='자기소개')),
                ('followings', models.ManyToManyField(blank=True, related_name='followers', to='users.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL, verbose_name='회원')),
            ],
        ),
        migrations.CreateModel(
            name='OauthId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255, verbose_name='토큰')),
                ('provider', models.CharField(max_length=255, verbose_name='구분자')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='회원')),
            ],
        ),
        migrations.CreateModel(
            name='ManagedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='회원')),
            ],
        ),
        migrations.CreateModel(
            name='LoggedIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_ip', models.GenericIPAddressField(null=True, verbose_name='로그인한 IP')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='로그인 기록')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='회원')),
            ],
        ),
        migrations.CreateModel(
            name='ConfirmPhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_number', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9999)], verbose_name='인증 번호')),
                ('expired_at', models.DateTimeField(verbose_name='만료일')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='회원')),
            ],
        ),
        migrations.CreateModel(
            name='ConfirmEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secured_key', models.CharField(default=0, max_length=255, verbose_name='시크릿 키')),
                ('expired_at', models.DateTimeField(auto_now_add=True, verbose_name='만료일')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='회원')),
            ],
        ),
    ]
