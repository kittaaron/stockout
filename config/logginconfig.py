import logging
import logging.config

__author__ = 'kittaaron'

log_filename = "/Users/kittaaron/git/stockout/logging.log"
logging.basicConfig(level=logging.DEBUG,
            format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename = log_filename,
                    filemode='a')

#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
#logging.getLogger('sqlalchemy.orm').setLevel(logging.INFO)

# 定义一个Handler打印INFO及以上级别的日志到sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 设置日志打印格式
formatter = logging.Formatter('%(name)s: %(levelname)s: %(message)s')
console.setFormatter(formatter)
# 将定义好的console日志handler添加到root logger
logging.getLogger('').addHandler(console)