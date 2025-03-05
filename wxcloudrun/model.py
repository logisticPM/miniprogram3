from datetime import datetime
from sqlalchemy.dialects.mysql import JSON

from wxcloudrun import db
from wxcloudrun.constants import ActivityStatus, RoomStatus, GrabStatus, LogLevel


# 计数表
class Counters(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Counters'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 用户表
class User(db.Model):
    __tablename__ = 'User'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(64), unique=True, nullable=False, index=True)
    nickname = db.Column(db.String(64))
    avatar_url = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean, default=False)
    admin_password = db.Column(db.String(128))
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    
    # 关系
    grab_records = db.relationship('GrabRecord', backref='user', lazy='dynamic')
    system_logs = db.relationship('SystemLog', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.nickname}>'


# 活动表
class Activity(db.Model):
    __tablename__ = 'Activity'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    status = db.Column(db.String(20), default=ActivityStatus.NOT_STARTED)
    building_name = db.Column(db.String(128))
    building_address = db.Column(db.String(255))
    location = db.Column(db.String(255))
    cover_image = db.Column(db.String(255))
    access_password = db.Column(db.String(64))
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    
    # 关系
    room_types = db.relationship('RoomType', backref='activity', lazy='dynamic')
    rooms = db.relationship('Room', backref='activity', lazy='dynamic')
    
    def __repr__(self):
        return f'<Activity {self.name}>'


# 房间类型表
class RoomType(db.Model):
    __tablename__ = 'RoomType'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('Activity.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    base_price = db.Column(db.Numeric(10, 2), nullable=False)
    area = db.Column(db.Numeric(8, 2))  # 面积，单位平方米
    features = db.Column(db.Text)  # 特点描述
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    
    # 关系
    rooms = db.relationship('Room', backref='room_type', lazy='dynamic')
    
    def __repr__(self):
        return f'<RoomType {self.name}>'


# 房间表
class Room(db.Model):
    __tablename__ = 'Room'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('Activity.id'), nullable=False)
    room_type_id = db.Column(db.Integer, db.ForeignKey('RoomType.id'), nullable=False)
    room_number = db.Column(db.String(20), nullable=False)
    floor = db.Column(db.Integer)
    orientation = db.Column(db.String(20))  # 朝向，如东、南、西、北
    actual_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default=RoomStatus.AVAILABLE)
    image_urls = db.Column(JSON)  # 存储多张图片URL的JSON数组
    details = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    
    # 关系
    grab_records = db.relationship('GrabRecord', backref='room', lazy='dynamic')
    
    def __repr__(self):
        return f'<Room {self.room_number}>'


# 抢购记录表
class GrabRecord(db.Model):
    __tablename__ = 'GrabRecord'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('Room.id'), nullable=False)
    status = db.Column(db.String(20), default=GrabStatus.PENDING)
    grab_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    confirm_time = db.Column(db.TIMESTAMP)
    cancel_time = db.Column(db.TIMESTAMP)
    notes = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    
    def __repr__(self):
        return f'<GrabRecord {self.id}>'


# 系统日志表
class SystemLog(db.Model):
    __tablename__ = 'SystemLog'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    level = db.Column(db.String(20), default=LogLevel.INFO)
    message = db.Column(db.Text, nullable=False)
    request_path = db.Column(db.String(255))
    request_method = db.Column(db.String(10))
    request_ip = db.Column(db.String(64))
    request_data = db.Column(JSON)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    
    def __repr__(self):
        return f'<SystemLog {self.id}>'
