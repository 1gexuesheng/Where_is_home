from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
    site_header = "One day of learn"
    site_title = "One day of learn 管理后台"
    index_title = '首页'

custom_site = CustomSite(name='cus_admin')
