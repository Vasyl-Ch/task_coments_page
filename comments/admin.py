from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "email", "parent", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user_name", "email", "text")
    raw_id_fields = ("parent",)
