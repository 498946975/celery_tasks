from __future__ import absolute_import
import os

from celery import Celery


class MyCelery(Celery):
    def gen_task_name(self, name, module):
        if module.endswith(".tasks"):
            module = module[:-6]
        return super(MyCelery, self).gen_task_name(name, module)


if not os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ["DJANGO_SETTINGS_MODULE"] = 'AlarMagnify.settings.prod'
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
celery_app = MyCelery("alarm")  # 创建celery应用
celery_app.config_from_object('celery_tasks.config')  # 配置celery
celery_app.autodiscover_tasks(['celery_tasks.inspection'], force=False)  # 设置APP自动加载任务， 从已经安装的APP中查找任务
