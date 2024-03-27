from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["headline", "reporter", "publish", "status"]
    list_filter = ["publish", "reporter", "status", "created"]
    search_fields = ["headline", "content"]
    raw_id_fields = ["reporter"]
    date_hierarchy = "publish"
    ordering = ["publish", "status"]
    prepopulated_fields = {"slug": ("headline",)}
