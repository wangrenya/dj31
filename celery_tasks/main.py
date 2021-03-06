
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dj31.settings.dev'

from  celery   import Celery

#创建实例
celery_app = Celery('sms_code')
#加载对象
celery_app.config_from_object('celery_tasks.config')

#注册对象

celery_app.autodiscover_tasks(['celery_tasks.sms'])