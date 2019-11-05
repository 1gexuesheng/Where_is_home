from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from .models import Post, Tag, Category
from config.models import SideBar
def post_list(request, category_id = None, tag_id = None):
    # 1
    # content = f'post_list category_id = {category_id}, tage_id={tag_id}'
    # return HttpResponse(content)

    # 2
    # return render(request, 'blog/list.html', context={'name': 'post_list'})

    # 3
    # if tag_id:
    #     try:
    #         tag = Tag.objects.get(id=tag_id)
    #     except Tag.DoesNotExist:
    #         post_list = []
    #     else:
    #         post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    # else:
    #     post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
    #     if category_id:
    #         post_list = post_list.filter(category_id=category_id)
    # return render(request, 'blog/list.html', context={'post_list': post_list})

    # 4 改3
    # tag = None
    # category = None
    # if tag_id:
    #     try:
    #         tag = Tag.objects.get(id=tag_id)
    #     except Tag.DoesNotExist:
    #         post_list = []
    #     else:
    #         post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    # else:
    #     post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
    #     if category_id:
    #         try:
    #             category = Category.objects.get(id=category_id)
    #         except Category.DoesNotExist:
    #             post_list = post_list.filter(category_id=category_id)

    # 5 使用model里写的函数
    tag = None
    category = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category)
    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,   # 分类
        'tag': tag,    # 标签
        'post_list': post_list,  # 文章
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    # return HttpResponse('detail')
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'config/detail.html', context=context)
