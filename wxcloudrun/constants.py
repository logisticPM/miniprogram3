"""
常量定义模块，用于减少硬编码字符串
"""

# 活动状态
class ActivityStatus:
    NOT_STARTED = 'NOT_STARTED'  # 未开始
    IN_PROGRESS = 'IN_PROGRESS'  # 进行中
    ENDED = 'ENDED'  # 已结束

# 房间状态
class RoomStatus:
    AVAILABLE = 'AVAILABLE'  # 可抢购
    GRABBED = 'GRABBED'  # 已抢购
    SOLD = 'SOLD'  # 已售出

# 抢购记录状态
class GrabStatus:
    PENDING = 'PENDING'  # 待确认
    CONFIRMED = 'CONFIRMED'  # 已确认
    CANCELLED = 'CANCELLED'  # 已取消

# 日志级别
class LogLevel:
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

# API响应码
class ResponseCode:
    SUCCESS = 0  # 成功
    PARAM_ERROR = 1  # 参数错误
    NOT_FOUND = 2  # 资源不存在
    FORBIDDEN = 3  # 权限不足
    SYSTEM_ERROR = 4  # 系统错误
    BUSINESS_ERROR = 5  # 业务错误
