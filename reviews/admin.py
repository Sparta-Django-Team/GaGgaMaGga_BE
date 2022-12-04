from django.contrib import admin

from .models import Review, Comment, Recomment

class CommentInline(admin.StackedInline):
    model = Comment
    
class RecommntInline(admin.StackedInline):
    model = Recomment

class ReviewAdmin(admin.ModelAdmin):
    inlines = (
        CommentInline,
    )
class CommentAdmin(admin.ModelAdmin):
    inlines = (
        RecommntInline,
    )
    
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Recomment)