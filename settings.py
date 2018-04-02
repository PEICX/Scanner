

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUGSWITCH = 0 # 0关闭调试，1开启调试
DEFAULT_ENCODING = "utf-8" # 编码



'''Celery相关设置'''
# 每个worker执行了多少任务就会死掉
# CELERYD_MAX_TASKS_PER_CHILD = 40
# ROOT启动
# platforms.C_FORCE_ROOT = True


# 'default_user_agent' or 'random_user_agent'
USER_AGENT = 'random_user_agent'
# COOKIES为True时，则跟踪cookie，此功能暂时失效
COOKIES = True
PROXIES = ""


# 自动填充表单的知识库设置
PARAMETER_NAME_KNOWLEDGE = {
    'scanner': ['username', 'user', 'uname', 'userid', 'nickname', 'logname', 'name', 'lastname', 'firstname'],
    'abc123456': ['pass', 'word', 'pswd', 'pwd', 'auth', 'password'],
    'test@qq.com': ['mail', 'email', 'e-mail'],
    'www.test.com': ['domain'],
    'http://www.test.com/': ['link', 'target', 'url', 'website', 'website'],
    'Just For A Test!': ['content', 'text', 'words', 'query', 'search', 'keyword', 'title', 'desc', 'data', 'payload',
                         'answer', 'description', 'descripcion', 'message', 'excerpt', 'comment'],
    'www.baidu.com': ['domain']
}





