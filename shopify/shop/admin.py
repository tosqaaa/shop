from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    list_display = ('title', 'slug', 'parent')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'brand', 'price', 'available', 'created_at', 'updated_at')
    fields = ('title', 'slug', 'price', 'brand', 'category', 'description', 'image', 'available')
    list_filter = ('available', 'created_at', 'updated_at', 'category')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    ordering = ('created_at',)
