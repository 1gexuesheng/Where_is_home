# 之后把数据库的配置剪切粘贴到 develop.py 中，然后 develop.py 文件的最上面引人 base
# 所有配 完整 develop.py 件如下：
from .base import *  # NOQA

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}