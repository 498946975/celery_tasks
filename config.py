from kombu import Queue, Exchange
from celery.schedules import crontab


"""redis相关设置"""
ENV = "127.0.0.1:8000"
BROKER_URL = f"redis://{ENV}/12"
CELERY_RESULT_BACKEND = f"redis//{ENV}/13"  # 指定结果的接收地址
CELERYD_FORCE_EXECV = True  # 非常重要，有些情况下可以防止死锁
# CELERY_CREATE_MISSING_QUEUES = True # 某个程序中出现的队列， 在broker中不存在， 则立刻创建它
CELERY_ACKS_LATE = True  # 任务失败允许重试， 对性能会稍微有影响

"""结果相关"""
CELERY_TASK_SERIALIZER = 'json'  # 指定任务序列化方式
CELERY_RESULT_SERIALIZER = 'json'  # 指定结果序列化方式
CELERY_MESSAGE_COMPRESSION = "zlib"  # 压缩方案选择，可以是zlib, bzip2, 默认是发生没有压缩的数据
CELERY_ACCEPT_CONTENT = ['json']  # Ignore other content
CELERY_TIMEZONE = "Asia/Shanghai"  # 设置时区
CELERY_ENABLE_UTC = True  # 启动时区设置celery使用的是UTC时区

"""并发相关"""
CELERY_REDIS_MAX_CONNECTIONS = 4  # celery worker每次去redis取任务的数量， 默认值是4
CELERYD_CONCURRECY = 20  # 并发worker数， 一般根据cpu数量来设定
BROK_TRANSPORT_OPTIONS = {'vi sibility timeout': 5}  # 5min
CELERY_ANNOTATIONS = {'*': {"rate_limit": "10/s"}}  # 限制所有的任务的刷新频率
CELERY_TASK_RESULT_EXPIRES = 15*60  # 任务结果过期时间设置
CELERYD_TASK_TIME_LIMIT = 15*60  # 单个任务运行的最大时间， 超过这个时间，task就会被kill， 自动交给父进程
CELERYD_MAX_TASKS_PER_CHILD = 40  # 每个worker最大执行的任务数量， 超过这个就将worker进行销毁， 防止内存泄漏
CELERY_DISABLE_RATE_LIMITS = True  # 任务发出后， 经过一段时间还未到acknowledge， 就将任务重新交给其他worker执行，关闭限速

# 任务队列， 防止相互影响
CELERY_QUEUES = (  # 设置execute队列， 绑定routing_key
    Queue('default', routing_key='default'),
    Queue("定时更新AthenaBI_queue", Exchange('for_定时更新AthenaBI_crontab'), routing_key="for_定时更新AthenaBI_router"),
    Queue("异步任务解析告警_queue", Exchange('for_异步任务解析告警_crontab', routing_key="for_异步任务解析告警_router"))
)

CELERY_ROUTES = {
    "定时更新AthenaBI": {
        "queue": "定时任务1_queue",
        "routing_key": "for_定时任务1_router"
    },
    "异步任务解析告警": {
        "queue": "异步任务解析告警_queue",
        "routing_key": "for_异步任务解析告警_router"
    }
}

# 定时任务
CELERY_BEAT_SCHEDULE = {
    "每天零点执行一次": {
        "task": "定时更新AthenaBI",
        "schedule": crontab(minute=0, hour=0, day_of_week="*/1"),  # 每天零点执行
        "args": (),  # 入参
        "option": {"queue": "定时更新AthenaBI_queue", "routing_key": "for_定时更新AthenaBI_router"}
    }
}
