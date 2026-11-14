from django.contrib import admin
from .models import Car, Comment


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'brand', 'price', 'quantity']
    list_filter = ['brand']
    search_fields = ['model']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_on']
