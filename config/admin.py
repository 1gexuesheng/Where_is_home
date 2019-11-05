# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import Link, SideBar
from jianchi.custom_site import custom_site
from jianchi.base_admin import BaseOwnerAdmin

# @admin.register(Link)
@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)

# @admin.register(SideBar)
@admin.register(SideBar, site=custom_site)
class SiderBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SiderBarAdmin, self).save_model(request, obj, form, change)
