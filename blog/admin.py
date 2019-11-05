# 最上面增加import
from django.contrib.admin.models import LogEntry

from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag

# 另一个后台
from jianchi.custom_site import custom_site
# admin基类，保证每个唯一用户
from jianchi.base_admin import BaseOwnerAdmin

# 6.23 添加form
from .adminforms import PostAdminForm

# 6.25 在同一页面编辑关联数据
class PostInline(admin.TabularInline):  # stackedInline 样式不同
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post

# @admin.register(Category)
@admin.register(Category, site=custom_site)
# class CategoryAdmin(admin.ModelAdmin):  # admin.ModelAdmin什么意思
class CategoryAdmin(BaseOwnerAdmin):  # admin.ModelAdmin什么意思

    list_display = ('name', 'status', 'is_nav', 'created_time')
    fields = ('name', 'status', 'is_nav')
    # 6.25 在同一页面编辑关联数据
    inlines = [PostInline, ]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

# @admin.register(Tag)
@admin.register(Tag, site=custom_site)
# class TagAdmin(admin.ModelAdmin):  # admin.ModelAdmin什么意思
class TagAdmin(BaseOwnerAdmin):  # admin.ModelAdmin什么意思
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

# username：liuyang   password:5shiliuyang


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category'
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset

# @admin.register(Post)
@admin.register(Post, site=custom_site)
# class PostAdmin(admin.ModelAdmin):
class PostAdmin(BaseOwnerAdmin):
    # 添加form管理的
    form = PostAdminForm

    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator',
    ]
    list_display_links = []
    # list_filter = ['category']
    # 上面的自定义的过滤器，用来只显示自己创建的分类
    list_filter = [CategoryOwnerFilter]

    search_fields = ['title', 'category__name']
    # actions_on_top = True
    # actions_on_bottom = True

    # 编辑页面
    # save_on_top = True

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag', ),
        })
    )
    # 横向的展示展示字段，
    filter_horizontal = ('tag',)
    # filter_vertical = ('tag',)

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('admin:blog_post_change', args=(obj.id,))
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    # 自定义显示列表页只能看到自己创建的文章
    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    # 自定义静态资源引入

    # class Media:
    #     css = {
    #         'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/'
    #                 'bootstrap.min.css', ),
    #     }
        # js = ('https://cdn.bootcss.com/jquery/3.4.1/jquery.min.js',)
        #       'https://cdn.bootcss.com/popper.js/1.15.0/esm/popper.js',
        #       'https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )



# 文件最下方增加
@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user',
                    'change_message']
