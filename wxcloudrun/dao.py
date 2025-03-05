import logging
from datetime import datetime

from sqlalchemy.exc import OperationalError
from sqlalchemy import desc, asc

from wxcloudrun import db
from wxcloudrun.model import Counters, User, Activity, RoomType, Room, GrabRecord, SystemLog
from wxcloudrun.constants import ActivityStatus, RoomStatus, GrabStatus, LogLevel, ResponseCode

# 初始化日志
logger = logging.getLogger('log')


# Counter 相关操作
def query_counterbyid(id):
    """
    根据ID查询Counter实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return Counters.query.filter(Counters.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def delete_counterbyid(id):
    """
    根据ID删除Counter实体
    :param id: Counter的ID
    """
    try:
        counter = Counters.query.get(id)
        if counter is None:
            return
        db.session.delete(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_counterbyid errorMsg= {} ".format(e))


def insert_counter(counter):
    """
    插入一个Counter实体
    :param counter: Counters实体
    """
    try:
        db.session.add(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def update_counterbyid(counter):
    """
    根据ID更新counter的值
    :param counter实体
    """
    try:
        counter = query_counterbyid(counter.id)
        if counter is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))


# User 相关操作
def get_or_create_user(openid, nickname=None, avatar_url=None):
    """
    根据openid获取用户，如果不存在则创建
    :param openid: 微信openid
    :param nickname: 用户昵称
    :param avatar_url: 用户头像URL
    :return: User实体
    """
    try:
        user = User.query.filter_by(openid=openid).first()
        if user is None:
            user = User(openid=openid, nickname=nickname, avatar_url=avatar_url)
            db.session.add(user)
            db.session.commit()
        return user
    except OperationalError as e:
        logger.error("get_or_create_user errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def get_user_by_id(user_id):
    """
    根据ID获取用户
    :param user_id: 用户ID
    :return: User实体
    """
    try:
        return User.query.get(user_id)
    except OperationalError as e:
        logger.error("get_user_by_id errorMsg= {} ".format(e))
        return None


def get_user_by_openid(openid):
    """
    根据openid获取用户
    :param openid: 微信openid
    :return: User实体
    """
    try:
        return User.query.filter_by(openid=openid).first()
    except OperationalError as e:
        logger.error("get_user_by_openid errorMsg= {} ".format(e))
        return None


def update_user(user):
    """
    更新用户信息
    :param user: User实体
    :return: 更新后的User实体
    """
    try:
        user.updated_at = datetime.now()
        db.session.commit()
        return user
    except OperationalError as e:
        logger.error("update_user errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def get_admin_users():
    """
    获取所有管理员用户
    :return: 管理员用户列表
    """
    try:
        return User.query.filter_by(is_admin=True).all()
    except OperationalError as e:
        logger.error("get_admin_users errorMsg= {} ".format(e))
        return []


# Activity 相关操作
def create_activity(activity):
    """
    创建活动
    :param activity: Activity实体
    :return: 创建的Activity实体
    """
    try:
        db.session.add(activity)
        db.session.commit()
        return activity
    except OperationalError as e:
        logger.error("create_activity errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def get_activity_by_id(activity_id):
    """
    根据ID获取活动
    :param activity_id: 活动ID
    :return: Activity实体
    """
    try:
        return Activity.query.get(activity_id)
    except OperationalError as e:
        logger.error("get_activity_by_id errorMsg= {} ".format(e))
        return None


def get_activities(status=None, limit=None, offset=None):
    """
    获取活动列表
    :param status: 活动状态过滤
    :param limit: 限制返回数量
    :param offset: 偏移量
    :return: 活动列表
    """
    try:
        query = Activity.query
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(desc(Activity.start_time))
        
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
            
        return query.all()
    except OperationalError as e:
        logger.error("get_activities errorMsg= {} ".format(e))
        return []


def update_activity(activity):
    """
    更新活动信息
    :param activity: Activity实体
    :return: 更新后的Activity实体
    """
    try:
        activity.updated_at = datetime.now()
        db.session.commit()
        return activity
    except OperationalError as e:
        logger.error("update_activity errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def delete_activity(activity_id):
    """
    删除活动
    :param activity_id: 活动ID
    :return: 是否成功
    """
    try:
        activity = Activity.query.get(activity_id)
        if activity is None:
            return False
        db.session.delete(activity)
        db.session.commit()
        return True
    except OperationalError as e:
        logger.error("delete_activity errorMsg= {} ".format(e))
        db.session.rollback()
        return False


# RoomType 相关操作
def create_room_type(room_type):
    """
    创建房间类型
    :param room_type: RoomType实体
    :return: 创建的RoomType实体
    """
    try:
        db.session.add(room_type)
        db.session.commit()
        return room_type
    except OperationalError as e:
        logger.error("create_room_type errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def get_room_type_by_id(room_type_id):
    """
    根据ID获取房间类型
    :param room_type_id: 房间类型ID
    :return: RoomType实体
    """
    try:
        return RoomType.query.get(room_type_id)
    except OperationalError as e:
        logger.error("get_room_type_by_id errorMsg= {} ".format(e))
        return None


def get_room_types_by_activity(activity_id):
    """
    获取活动下的所有房间类型
    :param activity_id: 活动ID
    :return: 房间类型列表
    """
    try:
        return RoomType.query.filter_by(activity_id=activity_id).all()
    except OperationalError as e:
        logger.error("get_room_types_by_activity errorMsg= {} ".format(e))
        return []


def update_room_type(room_type):
    """
    更新房间类型
    :param room_type: RoomType实体
    :return: 更新后的RoomType实体
    """
    try:
        room_type.updated_at = datetime.now()
        db.session.commit()
        return room_type
    except OperationalError as e:
        logger.error("update_room_type errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def delete_room_type(room_type_id):
    """
    删除房间类型
    :param room_type_id: 房间类型ID
    :return: 是否成功
    """
    try:
        room_type = RoomType.query.get(room_type_id)
        if room_type is None:
            return False
        db.session.delete(room_type)
        db.session.commit()
        return True
    except OperationalError as e:
        logger.error("delete_room_type errorMsg= {} ".format(e))
        db.session.rollback()
        return False


# Room 相关操作
def create_room(room):
    """
    创建房间
    :param room: Room实体
    :return: 创建的Room实体
    """
    try:
        db.session.add(room)
        db.session.commit()
        return room
    except OperationalError as e:
        logger.error("create_room errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def get_room_by_id(room_id):
    """
    根据ID获取房间
    :param room_id: 房间ID
    :return: Room实体
    """
    try:
        return Room.query.get(room_id)
    except OperationalError as e:
        logger.error("get_room_by_id errorMsg= {} ".format(e))
        return None


def get_rooms(activity_id=None, room_type_id=None, status=None, limit=None, offset=None):
    """
    获取房间列表
    :param activity_id: 活动ID过滤
    :param room_type_id: 房间类型ID过滤
    :param status: 房间状态过滤
    :param limit: 限制返回数量
    :param offset: 偏移量
    :return: 房间列表
    """
    try:
        query = Room.query
        
        if activity_id:
            query = query.filter_by(activity_id=activity_id)
        if room_type_id:
            query = query.filter_by(room_type_id=room_type_id)
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(asc(Room.room_number))
        
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
            
        return query.all()
    except OperationalError as e:
        logger.error("get_rooms errorMsg= {} ".format(e))
        return []


def update_room(room):
    """
    更新房间信息
    :param room: Room实体
    :return: 更新后的Room实体
    """
    try:
        room.updated_at = datetime.now()
        db.session.commit()
        return room
    except OperationalError as e:
        logger.error("update_room errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def delete_room(room_id):
    """
    删除房间
    :param room_id: 房间ID
    :return: 是否成功
    """
    try:
        room = Room.query.get(room_id)
        if room is None:
            return False
        db.session.delete(room)
        db.session.commit()
        return True
    except OperationalError as e:
        logger.error("delete_room errorMsg= {} ".format(e))
        db.session.rollback()
        return False


# GrabRecord 相关操作
def create_grab_record(grab_record):
    """
    创建抢购记录
    :param grab_record: GrabRecord实体
    :return: 创建的GrabRecord实体
    """
    try:
        db.session.add(grab_record)
        db.session.commit()
        return grab_record
    except OperationalError as e:
        logger.error("create_grab_record errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def get_grab_record_by_id(grab_id):
    """
    根据ID获取抢购记录
    :param grab_id: 抢购记录ID
    :return: GrabRecord实体
    """
    try:
        return GrabRecord.query.get(grab_id)
    except OperationalError as e:
        logger.error("get_grab_record_by_id errorMsg= {} ".format(e))
        return None


def get_user_grab_records(user_id, status=None, limit=None, offset=None):
    """
    获取用户的抢购记录
    :param user_id: 用户ID
    :param status: 状态过滤
    :param limit: 限制返回数量
    :param offset: 偏移量
    :return: 抢购记录列表
    """
    try:
        query = GrabRecord.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(desc(GrabRecord.grab_time))
        
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
            
        return query.all()
    except OperationalError as e:
        logger.error("get_user_grab_records errorMsg= {} ".format(e))
        return []


def get_room_grab_records(room_id, status=None):
    """
    获取房间的抢购记录
    :param room_id: 房间ID
    :param status: 状态过滤
    :return: 抢购记录列表
    """
    try:
        query = GrabRecord.query.filter_by(room_id=room_id)
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(desc(GrabRecord.grab_time)).all()
    except OperationalError as e:
        logger.error("get_room_grab_records errorMsg= {} ".format(e))
        return []


def update_grab_record(grab_record):
    """
    更新抢购记录
    :param grab_record: GrabRecord实体
    :return: 更新后的GrabRecord实体
    """
    try:
        grab_record.updated_at = datetime.now()
        db.session.commit()
        return grab_record
    except OperationalError as e:
        logger.error("update_grab_record errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def cancel_grab_record(grab_id):
    """
    取消抢购记录
    :param grab_id: 抢购记录ID
    :return: 是否成功
    """
    try:
        grab_record = GrabRecord.query.get(grab_id)
        if grab_record is None:
            return False
        
        grab_record.status = GrabStatus.CANCELLED
        grab_record.cancel_time = datetime.now()
        grab_record.updated_at = datetime.now()
        
        # 更新房间状态为可用
        room = Room.query.get(grab_record.room_id)
        if room:
            room.status = RoomStatus.AVAILABLE
            room.updated_at = datetime.now()
        
        db.session.commit()
        return True
    except OperationalError as e:
        logger.error("cancel_grab_record errorMsg= {} ".format(e))
        db.session.rollback()
        return False


def confirm_grab_record(grab_id):
    """
    确认抢购记录
    :param grab_id: 抢购记录ID
    :return: 是否成功
    """
    try:
        grab_record = GrabRecord.query.get(grab_id)
        if grab_record is None:
            return False
        
        grab_record.status = GrabStatus.CONFIRMED
        grab_record.confirm_time = datetime.now()
        grab_record.updated_at = datetime.now()
        
        # 更新房间状态为已售
        room = Room.query.get(grab_record.room_id)
        if room:
            room.status = RoomStatus.SOLD
            room.updated_at = datetime.now()
        
        db.session.commit()
        return True
    except OperationalError as e:
        logger.error("confirm_grab_record errorMsg= {} ".format(e))
        db.session.rollback()
        return False


# SystemLog 相关操作
def create_system_log(log):
    """
    创建系统日志
    :param log: SystemLog实体
    :return: 创建的SystemLog实体
    """
    try:
        db.session.add(log)
        db.session.commit()
        return log
    except OperationalError as e:
        logger.error("create_system_log errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def log_system_event(level, message, user_id=None, request_path=None, request_method=None, request_ip=None, request_data=None):
    """
    记录系统事件
    :param level: 日志级别
    :param message: 日志消息
    :param user_id: 用户ID
    :param request_path: 请求路径
    :param request_method: 请求方法
    :param request_ip: 请求IP
    :param request_data: 请求数据
    :return: 创建的SystemLog实体
    """
    try:
        log = SystemLog(
            level=level,
            message=message,
            user_id=user_id,
            request_path=request_path,
            request_method=request_method,
            request_ip=request_ip,
            request_data=request_data
        )
        db.session.add(log)
        db.session.commit()
        return log
    except OperationalError as e:
        logger.error("log_system_event errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def get_system_logs(level=None, user_id=None, limit=100, offset=None):
    """
    获取系统日志
    :param level: 日志级别过滤
    :param user_id: 用户ID过滤
    :param limit: 限制返回数量
    :param offset: 偏移量
    :return: 系统日志列表
    """
    try:
        query = SystemLog.query
        
        if level:
            query = query.filter_by(level=level)
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        query = query.order_by(desc(SystemLog.created_at))
        
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
            
        return query.all()
    except OperationalError as e:
        logger.error("get_system_logs errorMsg= {} ".format(e))
        return []
