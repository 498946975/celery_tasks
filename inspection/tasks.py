import os
import django
import sys
import logging
import traceback

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRO_PATH = os.path.dirname(os.path.dirname(APP_PATH))
sys.path.append(APP_PATH)
sys.path.append(PRO_PATH)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AlarMagnify.settings.prod')  # 项目名称
django.setup()

from queue import Queue
from celery_tasks.main import celery_app

Q = Queue()

# 定时任务: 更新数据AthenaBI
@celery_app.task(name="定时更新AthenaBI")
def verify_Athenabi():
    try:
        "调用功能逻辑的代码"
        pass
    except Exception as error:
        logging.error(error)
        logging.error(str(traceback.format_exc()))


# 异步任务解析告警
@celery_app.task(name="异步任务解析告警")
def source_to_parse():
    """调用相关代码逻辑"""
    pass
