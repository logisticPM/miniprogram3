"""
房间类型管理控制器
"""
import logging
from flask import request, Blueprint

from wxcloudrun.model import RoomType
from wxcloudrun.dao import (
    create_room_type, get_room_type_by_id, get_room_types, 
    get_activity_by_id, update_room_type, delete_room_type
)
from wxcloudrun.response import make_succ_response, make_err_response
from wxcloudrun.constants import ResponseCode

# 初始化日志
logger = logging.getLogger('log')

# 创建蓝图
room_type_bp = Blueprint('room_type', __name__)


@room_type_bp.route('/api/room_types', methods=['GET'])
def list_room_types():
    """
    获取房间类型列表
    """
    try:
        # 获取查询参数
        activity_id = request.args.get('activity_id', type=int)
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        
        # 查询房间类型列表
        room_types = get_room_types(activity_id, limit, offset)
        
        # 构造响应数据
        result = []
        for room_type in room_types:
            result.append({
                'id': room_type.id,
                'activity_id': room_type.activity_id,
                'name': room_type.name,
                'description': room_type.description,
                'base_price': float(room_type.base_price),
                'area': float(room_type.area) if room_type.area else None,
                'features': room_type.features,
                'image_url': room_type.image_url,
                'created_at': room_type.created_at,
                'updated_at': room_type.updated_at
            })
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("获取房间类型列表失败: {}".format(e))
        return make_err_response("获取房间类型列表失败")


@room_type_bp.route('/api/room_types/<int:room_type_id>', methods=['GET'])
def get_room_type(room_type_id):
    """
    获取房间类型详情
    """
    try:
        # 查询房间类型
        room_type = get_room_type_by_id(room_type_id)
        if room_type is None:
            return make_err_response("房间类型不存在", ResponseCode.NOT_FOUND)
        
        # 构造响应数据
        result = {
            'id': room_type.id,
            'activity_id': room_type.activity_id,
            'name': room_type.name,
            'description': room_type.description,
            'base_price': float(room_type.base_price),
            'area': float(room_type.area) if room_type.area else None,
            'features': room_type.features,
            'image_url': room_type.image_url,
            'created_at': room_type.created_at,
            'updated_at': room_type.updated_at
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("获取房间类型详情失败: {}".format(e))
        return make_err_response("获取房间类型详情失败")


@room_type_bp.route('/api/room_types', methods=['POST'])
def create_new_room_type():
    """
    创建房间类型
    """
    try:
        # 获取请求参数
        params = request.get_json()
        
        # 参数校验
        if not params.get('activity_id'):
            return make_err_response("活动ID不能为空", ResponseCode.PARAM_ERROR)
        
        if not params.get('name'):
            return make_err_response("房间类型名称不能为空", ResponseCode.PARAM_ERROR)
        
        if not params.get('base_price'):
            return make_err_response("基础价格不能为空", ResponseCode.PARAM_ERROR)
        
        # 检查活动是否存在
        activity = get_activity_by_id(params.get('activity_id'))
        if activity is None:
            return make_err_response("活动不存在", ResponseCode.NOT_FOUND)
        
        # 创建房间类型对象
        room_type = RoomType()
        room_type.activity_id = params.get('activity_id')
        room_type.name = params.get('name')
        room_type.description = params.get('description')
        room_type.base_price = params.get('base_price')
        room_type.area = params.get('area')
        room_type.features = params.get('features', [])
        room_type.image_url = params.get('image_url')
        
        # 保存房间类型
        room_type = create_room_type(room_type)
        if room_type is None:
            return make_err_response("创建房间类型失败")
        
        # 构造响应数据
        result = {
            'id': room_type.id,
            'name': room_type.name
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("创建房间类型失败: {}".format(e))
        return make_err_response("创建房间类型失败")


@room_type_bp.route('/api/room_types/<int:room_type_id>', methods=['PUT'])
def update_room_type_info(room_type_id):
    """
    更新房间类型
    """
    try:
        # 获取请求参数
        params = request.get_json()
        
        # 查询房间类型
        room_type = get_room_type_by_id(room_type_id)
        if room_type is None:
            return make_err_response("房间类型不存在", ResponseCode.NOT_FOUND)
        
        # 更新房间类型信息
        if 'name' in params:
            room_type.name = params.get('name')
        
        if 'description' in params:
            room_type.description = params.get('description')
        
        if 'base_price' in params:
            room_type.base_price = params.get('base_price')
        
        if 'area' in params:
            room_type.area = params.get('area')
        
        if 'features' in params:
            room_type.features = params.get('features')
        
        if 'image_url' in params:
            room_type.image_url = params.get('image_url')
        
        # 保存房间类型
        room_type = update_room_type(room_type)
        if room_type is None:
            return make_err_response("更新房间类型失败")
        
        # 构造响应数据
        result = {
            'id': room_type.id,
            'name': room_type.name
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("更新房间类型失败: {}".format(e))
        return make_err_response("更新房间类型失败")


@room_type_bp.route('/api/room_types/<int:room_type_id>', methods=['DELETE'])
def delete_room_type_by_id(room_type_id):
    """
    删除房间类型
    """
    try:
        # 查询房间类型
        room_type = get_room_type_by_id(room_type_id)
        if room_type is None:
            return make_err_response("房间类型不存在", ResponseCode.NOT_FOUND)
        
        # 删除房间类型
        success = delete_room_type(room_type_id)
        if not success:
            return make_err_response("删除房间类型失败")
        
        return make_succ_response({"id": room_type_id})
    except Exception as e:
        logger.error("删除房间类型失败: {}".format(e))
        return make_err_response("删除房间类型失败")
