from django.contrib import admin
from .models import ContentVersion

@admin.register(ContentVersion)
class ContentVersionAdmin(admin.ModelAdmin):
    list_display = ("content_id", "version", "timestamp")
    readonly_fields = ("metrics",)