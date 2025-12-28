from django.contrib import admin
from .models import Template

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "category", "is_active")
	list_filter = ("category", "is_active")
	search_fields = ("title", "description", "category")
