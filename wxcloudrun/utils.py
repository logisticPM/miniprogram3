"""
工具函数模块
"""
import json
from datetime import datetime, date
from decimal import Decimal
from flask import jsonify

from wxcloudrun.constants import ResponseCode, ActivityStatus


class CustomJSONEncoder(json.JSONEncoder):
    """
    自定义JSON编码器，用于处理特殊类型的序列化
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return super(CustomJSONEncoder, self).default(obj)


def api_response(code=ResponseCode.SUCCESS, data=None, error_msg=None):
    """
    统一API响应格式
    :param code: 响应码
    :param data: 响应数据
    :param error_msg: 错误信息
    :return: JSON响应
    """
    response = {
        'code': code,
        'data': data,
        'errorMsg': error_msg
    }
    return jsonify(response)


def format_activity_status(status):
    """
    格式化活动状态
    """
    status_map = {
        ActivityStatus.NOT_STARTED: "未开始",
        ActivityStatus.IN_PROGRESS: "进行中",
        ActivityStatus.ENDED: "已结束"
    }
    return status_map.get(status, "未知状态")


def format_room_status(status):
    """
    格式化房间状态为中文显示
    :param status: 房间状态
    :return: 中文状态
    """
    status_map = {
        'AVAILABLE': '可抢购',
        'GRABBED': '已抢购',
        'SOLD': '已售出'
    }
    return status_map.get(status, status)


def format_grab_status(status):
    """
    格式化抢购记录状态为中文显示
    :param status: 抢购记录状态
    :return: 中文状态
    """
    status_map = {
        'PENDING': '待确认',
        'CONFIRMED': '已确认',
        'CANCELLED': '已取消'
    }
    return status_map.get(status, status)


def get_activity_status_class(status):
    """
    获取活动状态对应的样式类
    """
    status_class_map = {
        ActivityStatus.NOT_STARTED: "status-not-started",
        ActivityStatus.IN_PROGRESS: "status-in-progress",
        ActivityStatus.ENDED: "status-ended"
    }
    return status_class_map.get(status, "")


def get_room_status_class(status):
    """
    获取房间状态对应的样式类
    :param status: 房间状态
    :return: 样式类名
    """
    class_map = {
        'AVAILABLE': 'status-available',
        'GRABBED': 'status-grabbed',
        'SOLD': 'status-sold'
    }
    return class_map.get(status, '')


def get_grab_status_class(status):
    """
    获取抢购记录状态对应的样式类
    :param status: 抢购记录状态
    :return: 样式类名
    """
    class_map = {
        'PENDING': 'status-pending',
        'CONFIRMED': 'status-confirmed',
        'CANCELLED': 'status-cancelled'
    }
    return class_map.get(status, '')


def update_activity_status(activity):
    """
    根据当前时间更新活动状态
    返回是否有状态变化
    """
    now = datetime.now()
    old_status = activity.status
    
    if now < activity.start_time:
        activity.status = ActivityStatus.NOT_STARTED
    elif now > activity.end_time:
        activity.status = ActivityStatus.ENDED
    else:
        activity.status = ActivityStatus.IN_PROGRESS
    
    return old_status != activity.status
