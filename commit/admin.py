from django.contrib import admin

# Register your models here.
from .models import Comment
from jianchi.custom_site import custom_site
from jianchi.base_admin import BaseOwnerAdmin
@admin.register(Comment, site=custom_site)
# @admin.register(Comment)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
