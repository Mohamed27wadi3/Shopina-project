from django.contrib import admin
from .models import Shop, ShopTheme

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "owner", "slug", "is_active", "is_verified")
	list_filter = ("is_active", "is_verified", "country", "city")
	search_fields = ("name", "slug", "owner__username", "email")

@admin.register(ShopTheme)
class ShopThemeAdmin(admin.ModelAdmin):
	list_display = ("id", "shop", "template_id", "is_active", "updated_at")
	list_filter = ("is_active",)
	search_fields = ("shop__slug",)
