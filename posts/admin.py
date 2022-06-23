from django.contrib import admin
from .models import *
from django.utils.html import format_html


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'category',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image',)


# class ProfileAdmin(admin.ModelAdmin):
#     def avatar(self, object):
#         return format_html(
#             '<img src="{}" width="40" style="border-radius:40px"/>'.format(
#                 object.image.url))

#     list_display = ('id', 'user')


# Register your models here.
class FollowCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'category',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(FollowCategory,FollowCategoryAdmin)
