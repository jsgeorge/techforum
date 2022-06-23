from django.contrib import admin
from .models import *
from django.utils.html import format_html

admin.site.register(Profile)
admin.site.register(UnivStudent)
admin.site.register(FollowUser)
