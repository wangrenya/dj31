from  dj31.utils.yuntongxun.sms import CCP
from celery_tesks.main import  celery_app
import  logging
logger = logging.getLogger('django')
#实现异步处理短信
#bind
#retry_backoff=3间隔时间
@celery_app.task(bind = True,name='send_sms_code',retry_backoff=3)
def send_sms_code(self,mobile,sms_code):
    try:
        send_res = CCP().send_template_sms(mobile,[sms_code,5],1)
    except Exception as  e:
      logger.error(e)
      raise self.retry(exc=e ,max_retries=3)
    if  send_res != 0:
        raise self.retry(exc=Exception('发送短信失败'), max_retries=3)

    return send_res