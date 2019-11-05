from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
            choices=STATUS_ITEMS, verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    # Category object的解决办法 --名字
    def __str__(self):
        return self.name

    #1分类。导航的函数 产生两次io的
    # @classmethod
    # def get_navs(cls):
    #     categories = cls.objects.filter(status=cls.STATUS_NORMAL)
    #     nav_categories = categories.filter(is_nav=True)
    #     normal_categories = categories.filter(is_nav=False)
    #     return {
    #         'navs': nav_categories,
    #         'categories': normal_categories,
    #     }

    # 重构版
    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }

class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                    choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name

class Post(models.Model):
    # 7.3.1调整模型
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须是MarkDowm格式')  # 下面的字提示
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
        choices=STATUS_ITEMS, verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']  # 根据id进行降序

    def __str__(self):
        return self.title

    # 获取最新文章标签post_list数据的操作
    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)    # 1
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:       # 1.先找到文章，通过标签，然后懒加载文章对应的用户和分类
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)\
            .select_related('owner', 'category')

        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            # print(category_id, type(category_id))   # None <class 'NoneType'>

            category = Category.objects.get(id=category_id)   # 可以但是 category_id 不可以
            print('category', category)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:

            post_list = category.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')
        print('get_by_category', post_list, category)
        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        #  没有return cls的函数
        print('latest_posts', queryset)
        return queryset
    # 7.3.1调整模型
    @classmethod
    def hot_posts(cls):
        print('hot_posts', cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv'))
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')
