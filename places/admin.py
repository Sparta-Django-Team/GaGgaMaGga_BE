from django.contrib import admin

from .models import Place
from reviews.models import Review


class ReviewInline(admin.StackedInline):
    model = Review


class PlacewAdmin(admin.ModelAdmin):
    inlines = (ReviewInline,)


admin.site.register(Place, PlacewAdmin)