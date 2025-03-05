# 创建应用实例
import sys
import logging

from wxcloudrun import app
from init_db import init_db

# 初始化日志
logger = logging.getLogger('log')

# 启动Flask Web服务
if __name__ == '__main__':
    # 初始化数据库
    logger.info("正在初始化数据库...")
    init_db()
    logger.info("数据库初始化完成，启动应用...")
    
    app.run(host=sys.argv[1], port=sys.argv[2])
