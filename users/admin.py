from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import (
    User,
    ConfirmEmail,
    ConfirmPhoneNumber,
    LoggedIn,
    Profile,
    OauthId,
    BlockedCountryIP,
)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput)
    password2 = forms.CharField(label="비밀번호 재확인", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ( "username", "email", "phone_number",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 맞지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class ConfirmEmailInline(admin.StackedInline):
    model = ConfirmEmail


class ConfirmPhoneNumberInline(admin.StackedInline):
    model = ConfirmPhoneNumber


class ProfileInline(admin.StackedInline):
    model = Profile


class BlockedCountryIPInline(admin.StackedInline):
    model = BlockedCountryIP


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ( "username", "password", "is_active", "is_admin", "email", "phone_number",)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ( "username", "email", "phone_number", "withdraw", "is_admin", "is_active", "is_confirmed", )
    list_filter = ("is_admin",)
    fieldsets = (
        (None,{"fields": ("username", "password", "email", "phone_number", )},),
        ("Permissions", {"fields": ("is_admin",)}),)

    add_fieldsets = (
        (None,{"classes": ("wide",),
            "fields": ("username", "password1", "password2", "email", "phone_number", ),},),)
    
    inlines = (
        ConfirmEmailInline,
        ConfirmPhoneNumberInline,
        ProfileInline,
        BlockedCountryIPInline,
    )
    
    search_fields = ("username", "email", "phone_number", )
    ordering = ("username",)
    filter_horizontal = ()


admin.site.register(OauthId)
admin.site.register(LoggedIn)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Profile)
