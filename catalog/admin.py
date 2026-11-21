from django.contrib import admin
from .models import Brand, Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "accent", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["is_active"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "brand", "category", "price", "stock_quantity", "is_active"]
    list_filter = ["category", "brand", "is_active", "is_featured", "is_new"]
    search_fields = ["name", "model", "description"]
    prepopulated_fields = {"slug": ("name",)}
