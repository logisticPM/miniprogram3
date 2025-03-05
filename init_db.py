import logging
from wxcloudrun import db
from wxcloudrun.model import Counters, User, Activity, RoomType, Room, GrabRecord, SystemLog

# 初始化日志
logger = logging.getLogger('log')

def init_db():
    """
    初始化数据库表结构
    """
    try:
        logger.info("开始初始化数据库...")
        # 创建所有表
        db.create_all()
        logger.info("数据库初始化成功！")
    except Exception as e:
        logger.error("数据库初始化失败: {}".format(e))

if __name__ == '__main__':
    init_db()
