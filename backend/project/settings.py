# coding:utf-8
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
"""
Django settings for project.
"""
import os
import sys
import datetime
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../.env'), override=True)
# 设置 apps, extra_apps 目录
sys.path.insert(0, BASE_DIR)
app_dir = os.path.join(BASE_DIR, 'apps')
sys.path.insert(0, app_dir)
APPS = os.listdir(app_dir)
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

DEBUG = True if os.environ.get('DEBUG') == 'True' else False

PROJECT_ZHNAME = os.environ.get('PROJECT_ZHNAME')
PROJECT_NAME = os.environ.get('PROJECT_NAME')
PROJECT_URL = os.environ.get('PROJECT_URL')
PROJECT_HOST = os.environ.get('PROJECT_HOST')
PROJECT_PORT = os.environ.get('PROJECT_PORT')

LOG_LEVEL = os.environ.get('LOG_LEVEL')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
ALLOW_EMAIL_DOMAIN = os.environ.get('ALLOW_EMAIL_DOMAIN')

TOKEN_NAME = os.environ.get('TOKEN_NAME')
SSO_CLIENT_ENABLE = True if os.environ.get('SSO_CLIENT_ENABLE') == 'True' else False

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

DATABASE = os.environ.get('DATABASE')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = int(os.environ.get('DB_PORT'))
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWD = os.environ.get('DB_PASSWD')

INIT_ADMIN_USERNAME = os.environ.get('INIT_ADMIN_USERNAME')
INIT_ADMIN_PASSWORD = os.environ.get('INIT_ADMIN_PASSWORD')

#开启双因子认证
MFA_ENABLE = True if os.environ.get('MFA_ENABLE') == 'True' else False


# mail
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True if os.environ.get('EMAIL_USE_SSL') == 'True' else False
EMAIL_TIMEOUT = 5
SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ldap
LDAP_ENABLE = True if os.environ.get('LDAP_ENABLE') == 'True' else False
LDAP_URI = os.environ.get('LDAP_URI')
LDAP_USER = os.environ.get('LDAP_USER')
LDAP_PASSWORD = os.environ.get('LDAP_PASSWORD')
BASE_DN = os.environ.get('BASE_DN')
USER_DN_FLAG = os.environ.get('USER_DN_FLAG')
USER_ATTR_LIST = os.environ.get('USER_ATTR_LIST').split(',')
GROUP_TYPE = os.environ.get('GROUP_TYPE')
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DjangoUeditor',
    'xadmin',
    'crispy_forms',
    'reversion',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'import_export',
    'imagekit',
    'social_django',
    'djcelery',
]
# 自动注册
INSTALLED_APPS.extend(['{}'.format(row) for row in APPS])


MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'crequest.middleware.CrequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.AuthMiddleware',
    'users.middleware.OtpAuthMiddleware',
    'users.middleware.UrlCheckMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../frontend/dist'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

if DATABASE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            'OPTIONS': {
                'autocommit': True,
                'charset': 'utf8',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'sqlite3.db'),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 设置时区
LANGUAGE_CODE = 'zh-hans'  # 中文支持，django1.8以后支持；1.8以前是zh-cn
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "../frontend/dist/static")

CORS_ORIGIN_ALLOW_ALL = True

# swagger 配置项
SWAGGER_SETTINGS = {
    # 基础样式
    'SECURITY_DEFINITIONS': {
        "basic": {
            'type': 'basic'
        }
    },
    # 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的.
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    # 'DOC_EXPANSION': None,
    # 'SHOW_REQUEST_HEADERS':True,
    # 'USE_SESSION_AUTH': True,
    # 'DOC_EXPANSION': 'list',
    # 接口文档中方法列表以首字母升序排列
    'APIS_SORTER': 'alpha',
    # 如果支持json提交, 则接口文档中包含json输入框
    'JSON_EDITOR': True,
    # 方法列表字母排序
    'OPERATIONS_SORTER': 'alpha',
    'VALIDATOR_URL': None,
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://:%(password)s@%(host)s:%(port)s/0' % {
            'password': REDIS_PASSWORD if REDIS_PASSWORD else '',
            'host': REDIS_HOST or '127.0.0.1',
            'port': REDIS_PORT or 6379,
        },
        "KEY_PREFIX": PROJECT_NAME,
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.auth.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    # 'DEFAULT_THROTTLE_CLASSES': (
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle'
    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '3/second',
    #     'user': '5/second'
    # },
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
}

JWT_AUTH = {
    'JWT_AUTH_COOKIE': TOKEN_NAME,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_ALLOW_REFRESH': True,
}

AUTH_USER_MODEL = 'users.UserProfile'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace("\\", "/")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] \
                      [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'}
    },
    'filters': {
    },
    'handlers': {
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/error.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 1,
            'formatter': 'standard'
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/all.log'),  # 日志输出文件
            'maxBytes': 1024 * 1024 * 100,  # 文件大小
            'backupCount': 1,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/request.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 1,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'views': {
            'handlers': ['default', 'error'],
            'level': 'INFO',
            'propagate': True
        }
    }

}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.weibo.WeiboOAuth2',
    'social_core.backends.qq.QQOAuth2',
    'social_core.backends.weixin.WeixinOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    # 'social_core.pipeline.user.get_username',
    # 'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    # 'social_core.pipeline.social_auth.associate_by_email',
)

SOCIAL_AUTH_WEIBO_KEY = os.environ.get('SOCIAL_AUTH_WEIBO_KEY')
SOCIAL_AUTH_WEIBO_SECRET = os.environ.get('SOCIAL_AUTH_WEIBO_SECRET')

SOCIAL_AUTH_QQ_KEY = os.environ.get('SOCIAL_AUTH_QQ_KEY')
SOCIAL_AUTH_QQ_SECRET = os.environ.get('SOCIAL_AUTH_QQ_SECRET')

SOCIAL_AUTH_WEIXIN_KEY = os.environ.get('SOCIAL_AUTH_WEIXIN_KEY')
SOCIAL_AUTH_WEIXIN_SECRET = os.environ.get('SOCIAL_AUTH_WEIXIN_SECRET')

SOCIAL_AUTH_GITHUB_KEY = os.environ.get('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('SOCIAL_AUTH_GITHUB_SECRET')

SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/api/v1/users/user/social_login_set_cookie/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/#/user/info'
SOCIAL_AUTH_GITHUB_EXTRA_DATA = [
    ('login', 'username'),
    ('avatar_url', 'profile_image_url'),
]

CONTENT_TYPE = {
    'csv': 'text/csv',
    'xls': 'application/vnd.ms-excel',
    'json': 'application/json',
    'yaml': 'text/yaml',
    'html': 'text/html',
}

# CELERY
import djcelery
from celery import platforms
from kombu import Exchange, Queue

platforms.C_FORCE_ROOT = True
djcelery.setup_loader()
BROKER_URL = 'redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT)  # redis broker
CELERY_RESULT_BACKEND = BROKER_URL  # redis backend
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # 定时任务
BROKER_CONNECTION_TIMEOUT = 30
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
CELERY_TASK_RESULT_EXPIRES = 7 * 86400
CELERY_SEND_EVENTS = False
CELERY_EVENT_QUEUE_EXPIRES = 60
CELERYD_LOG_FILE = os.path.join(BASE_DIR, 'logs/celery.log')
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, 'logs/celery_beat.log')
HIGH_PRIORITY_QUEUE = 'task_a'
LOW_PRIORITY_QUEUE = 'task_b'
CELERY_QUEUES = (
    Queue('task_a', Exchange('task_a'), routing_key='task_a'),  # 主动任务的队列
    Queue('task_b', Exchange('task_b'), routing_key='task_b')  # 定时任务的队列
)
CELERY_ROUTES = {
    'task.add': {'queue': 'task_a', 'routing_key': 'task_a'}
}
CELERY_DEFAULT_QUEUE = 'task_b'
CELERY_DEFAULT_EXCHANGE = 'task_b'
CELERY_DEFAULT_ROUTING_KEY = 'task_b'
