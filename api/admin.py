from django.contrib import admin
from .models import Article, UserProfile, ArticleLike, Comment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
     list_display = ("user", "first_name", "last_name", "profession", "created_at")
     search_fields = ("user__username", "first_name", "last_name", "profession")
     list_filter = ("created_at",)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
     list_display = ("title", "author", "status", "created_at", "updated_at", "display_tags")
     search_fields = ("title", "author__username", "tags__name")
     list_filter = ("status", "created_at", "updated_at")
     prepopulated_fields = {"title": ("title",)}

     def display_tags(self, obj):
          return ", ".join(tag.name for tag in obj.tags.all())

     display_tags.short_description = "Tags"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
     list_display = ("content", "author", "article", "created_at")
     search_fields = ("author__user__username", "content")
     list_filter = ("created_at",)

@admin.register(ArticleLike)
class ArticleLikeAdmin(admin.ModelAdmin):
     list_display = ("user", "article", "created_at")
     search_fields = ("user__user__username", "article__title")
     list_filter = ("created_at",)