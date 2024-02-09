from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Topic, Redactor, Newspaper, Comment, ReplyComment


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ["title", "display_topics"]
    list_filter = ["title"]
    search_fields = ["title"]

    def display_topics(self, obj):
        return ", ".join([topic.name for topic in obj.topic.all()])


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience", "profile_images")
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("bio", "profile_images", "years_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name", "profile_images", "bio", "years_of_experience",)}),
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ["name"]


admin.site.register(Comment)
admin.site.register(ReplyComment)
