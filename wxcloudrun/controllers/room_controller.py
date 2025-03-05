"""
房间管理控制器
"""
import logging
from flask import request, Blueprint

from wxcloudrun.model import Room
from wxcloudrun.dao import (
    create_room, get_room_by_id, get_rooms, get_activity_by_id,
    get_room_type_by_id, update_room, delete_room, create_grab_record,
    get_user_by_openid
)
from wxcloudrun.response import make_succ_response, make_err_response
from wxcloudrun.constants import ResponseCode, RoomStatus, GrabStatus
from wxcloudrun.model import GrabRecord

# 初始化日志
logger = logging.getLogger('log')

# 创建蓝图
room_bp = Blueprint('room', __name__)


@room_bp.route('/api/rooms', methods=['GET'])
def list_rooms():
    """
    获取房间列表
    """
    try:
        # 获取查询参数
        activity_id = request.args.get('activity_id', type=int)
        room_type_id = request.args.get('room_type_id', type=int)
        status = request.args.get('status')
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        
        # 查询房间列表
        rooms = get_rooms(activity_id, room_type_id, status, limit, offset)
        
        # 构造响应数据
        result = []
        for room in rooms:
            result.append({
                'id': room.id,
                'activity_id': room.activity_id,
                'room_type_id': room.room_type_id,
                'room_number': room.room_number,
                'floor': room.floor,
                'orientation': room.orientation,
                'actual_price': float(room.actual_price),
                'status': room.status,
                'image_urls': room.image_urls,
                'details': room.details,
                'created_at': room.created_at,
                'updated_at': room.updated_at
            })
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("获取房间列表失败: {}".format(e))
        return make_err_response("获取房间列表失败")


@room_bp.route('/api/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    """
    获取房间详情
    """
    try:
        # 查询房间
        room = get_room_by_id(room_id)
        if room is None:
            return make_err_response("房间不存在", ResponseCode.NOT_FOUND)
        
        # 查询关联的房间类型
        room_type = get_room_type_by_id(room.room_type_id)
        
        # 构造响应数据
        result = {
            'id': room.id,
            'activity_id': room.activity_id,
            'room_type_id': room.room_type_id,
            'room_number': room.room_number,
            'floor': room.floor,
            'orientation': room.orientation,
            'actual_price': float(room.actual_price),
            'status': room.status,
            'image_urls': room.image_urls,
            'details': room.details,
            'created_at': room.created_at,
            'updated_at': room.updated_at
        }
        
        # 添加房间类型信息
        if room_type:
            result['room_type'] = {
                'id': room_type.id,
                'name': room_type.name,
                'description': room_type.description,
                'base_price': float(room_type.base_price),
                'area': float(room_type.area) if room_type.area else None,
                'features': room_type.features,
                'image_url': room_type.image_url
            }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("获取房间详情失败: {}".format(e))
        return make_err_response("获取房间详情失败")


@room_bp.route('/api/rooms', methods=['POST'])
def create_new_room():
    """
    创建房间
    """
    try:
        # 获取请求参数
        params = request.get_json()
        
        # 参数校验
        if not params.get('activity_id'):
            return make_err_response("活动ID不能为空", ResponseCode.PARAM_ERROR)
        
        if not params.get('room_type_id'):
            return make_err_response("房间类型ID不能为空", ResponseCode.PARAM_ERROR)
        
        if not params.get('room_number'):
            return make_err_response("房间号不能为空", ResponseCode.PARAM_ERROR)
        
        if not params.get('actual_price'):
            return make_err_response("实际价格不能为空", ResponseCode.PARAM_ERROR)
        
        # 检查活动是否存在
        activity = get_activity_by_id(params.get('activity_id'))
        if activity is None:
            return make_err_response("活动不存在", ResponseCode.NOT_FOUND)
        
        # 检查房间类型是否存在
        room_type = get_room_type_by_id(params.get('room_type_id'))
        if room_type is None:
            return make_err_response("房间类型不存在", ResponseCode.NOT_FOUND)
        
        # 创建房间对象
        room = Room()
        room.activity_id = params.get('activity_id')
        room.room_type_id = params.get('room_type_id')
        room.room_number = params.get('room_number')
        room.floor = params.get('floor')
        room.orientation = params.get('orientation')
        room.actual_price = params.get('actual_price')
        room.status = RoomStatus.AVAILABLE
        room.image_urls = params.get('image_urls', [])
        room.details = params.get('details')
        
        # 保存房间
        room = create_room(room)
        if room is None:
            return make_err_response("创建房间失败")
        
        # 构造响应数据
        result = {
            'id': room.id,
            'room_number': room.room_number,
            'status': room.status
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("创建房间失败: {}".format(e))
        return make_err_response("创建房间失败")


@room_bp.route('/api/rooms/<int:room_id>', methods=['PUT'])
def update_room_info(room_id):
    """
    更新房间
    """
    try:
        # 获取请求参数
        params = request.get_json()
        
        # 查询房间
        room = get_room_by_id(room_id)
        if room is None:
            return make_err_response("房间不存在", ResponseCode.NOT_FOUND)
        
        # 更新房间信息
        if 'room_number' in params:
            room.room_number = params.get('room_number')
        
        if 'floor' in params:
            room.floor = params.get('floor')
        
        if 'orientation' in params:
            room.orientation = params.get('orientation')
        
        if 'actual_price' in params:
            room.actual_price = params.get('actual_price')
        
        if 'image_urls' in params:
            room.image_urls = params.get('image_urls')
        
        if 'details' in params:
            room.details = params.get('details')
        
        # 保存房间
        room = update_room(room)
        if room is None:
            return make_err_response("更新房间失败")
        
        # 构造响应数据
        result = {
            'id': room.id,
            'room_number': room.room_number,
            'status': room.status
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("更新房间失败: {}".format(e))
        return make_err_response("更新房间失败")


@room_bp.route('/api/rooms/<int:room_id>', methods=['DELETE'])
def delete_room_by_id(room_id):
    """
    删除房间
    """
    try:
        # 查询房间
        room = get_room_by_id(room_id)
        if room is None:
            return make_err_response("房间不存在", ResponseCode.NOT_FOUND)
        
        # 删除房间
        success = delete_room(room_id)
        if not success:
            return make_err_response("删除房间失败")
        
        return make_succ_response({"id": room_id})
    except Exception as e:
        logger.error("删除房间失败: {}".format(e))
        return make_err_response("删除房间失败")


@room_bp.route('/api/rooms/<int:room_id>/grab', methods=['POST'])
def grab_room(room_id):
    """
    抢购房间
    """
    try:
        # 获取请求参数
        params = request.get_json()
        
        # 参数校验
        if not params.get('openid'):
            return make_err_response("用户openid不能为空", ResponseCode.PARAM_ERROR)
        
        # 查询房间
        room = get_room_by_id(room_id)
        if room is None:
            return make_err_response("房间不存在", ResponseCode.NOT_FOUND)
        
        # 检查房间状态
        if room.status != RoomStatus.AVAILABLE:
            return make_err_response("房间已被抢购或已售出", ResponseCode.BUSINESS_ERROR)
        
        # 获取用户
        user = get_user_by_openid(params.get('openid'))
        if user is None:
            return make_err_response("用户不存在", ResponseCode.NOT_FOUND)
        
        # 创建抢购记录
        grab_record = GrabRecord()
        grab_record.user_id = user.id
        grab_record.room_id = room.id
        grab_record.status = GrabStatus.PENDING
        grab_record.notes = params.get('notes')
        
        # 保存抢购记录
        grab_record = create_grab_record(grab_record)
        if grab_record is None:
            return make_err_response("创建抢购记录失败")
        
        # 更新房间状态
        room.status = RoomStatus.GRABBED
        room = update_room(room)
        if room is None:
            return make_err_response("更新房间状态失败")
        
        # 构造响应数据
        result = {
            'id': grab_record.id,
            'user_id': grab_record.user_id,
            'room_id': grab_record.room_id,
            'status': grab_record.status,
            'grab_time': grab_record.grab_time
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("抢购房间失败: {}".format(e))
        return make_err_response("抢购房间失败")
