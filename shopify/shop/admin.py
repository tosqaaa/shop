from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'parent')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'brand', 'price', 'available', 'created_at', 'updated_at')
    fields = ('title', 'slug', 'price', 'brand', 'category', 'description', 'image', 'available')
    list_filter = ('available', 'created_at', 'updated_at')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    ordering = ('created_at',)
