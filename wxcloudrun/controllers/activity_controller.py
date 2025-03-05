"""
活动管理控制器
"""
import logging
from datetime import datetime
from flask import request, Blueprint

from wxcloudrun.model import Activity
from wxcloudrun.dao import (
    create_activity, get_activity_by_id, get_activities,
    update_activity, delete_activity
)
from wxcloudrun.response import make_succ_response, make_err_response
from wxcloudrun.constants import ResponseCode, ActivityStatus
from wxcloudrun.utils import update_activity_status

# 初始化日志
logger = logging.getLogger('log')

# 创建蓝图
activity_bp = Blueprint('activity', __name__)


@activity_bp.route('/api/activities', methods=['GET'])
def list_activities():
    """
    获取活动列表
    """
    try:
        # 获取查询参数
        status = request.args.get('status')
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        
        # 查询活动列表
        activities = get_activities(status, limit, offset)
        
        # 自动更新活动状态
        for activity in activities:
            if update_activity_status(activity):
                update_activity(activity)
        
        # 构造响应数据
        result = []
        for activity in activities:
            result.append({
                'id': activity.id,
                'name': activity.name,
                'description': activity.description,
                'start_time': activity.start_time,
                'end_time': activity.end_time,
                'status': activity.status,
                'building_name': activity.building_name,
                'building_address': activity.building_address,
                'location': activity.location,
                'cover_image': activity.cover_image,
                'created_at': activity.created_at,
                'updated_at': activity.updated_at
            })
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("获取活动列表失败: {}".format(e))
        return make_err_response("获取活动列表失败")


@activity_bp.route('/api/activities/<int:activity_id>', methods=['GET'])
def get_activity(activity_id):
    """
    获取活动详情
    """
    try:
        # 查询活动
        activity = get_activity_by_id(activity_id)
        if activity is None:
            return make_err_response("活动不存在", ResponseCode.NOT_FOUND)
        
        # 自动更新活动状态
        if update_activity_status(activity):
            update_activity(activity)
        
        # 构造响应数据
        result = {
            'id': activity.id,
            'name': activity.name,
            'description': activity.description,
            'start_time': activity.start_time,
            'end_time': activity.end_time,
            'status': activity.status,
            'building_name': activity.building_name,
            'building_address': activity.building_address,
            'location': activity.location,
            'cover_image': activity.cover_image,
            'access_password': activity.access_password,
            'created_at': activity.created_at,
            'updated_at': activity.updated_at
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("获取活动详情失败: {}".format(e))
        return make_err_response("获取活动详情失败")


@activity_bp.route('/api/activities', methods=['POST'])
def create_new_activity():
    """
    创建活动
    """
    try:
        # 获取请求参数
        params = request.get_json()
        
        # 参数校验
        if not params.get('name'):
            return make_err_response("活动名称不能为空", ResponseCode.PARAM_ERROR)
        
        if not params.get('start_time') or not params.get('end_time'):
            return make_err_response("活动开始时间和结束时间不能为空", ResponseCode.PARAM_ERROR)
        
        # 创建活动对象
        activity = Activity()
        activity.name = params.get('name')
        activity.description = params.get('description')
        activity.start_time = datetime.fromisoformat(params.get('start_time').replace('Z', '+00:00'))
        activity.end_time = datetime.fromisoformat(params.get('end_time').replace('Z', '+00:00'))
        activity.building_name = params.get('building_name')
        activity.building_address = params.get('building_address')
        activity.location = params.get('location')
        activity.cover_image = params.get('cover_image')
        activity.access_password = params.get('access_password')
        
        # 设置活动状态
        now = datetime.now()
        if now < activity.start_time:
            activity.status = ActivityStatus.NOT_STARTED
        elif now > activity.end_time:
            activity.status = ActivityStatus.ENDED
        else:
            activity.status = ActivityStatus.IN_PROGRESS
        
        # 保存活动
        activity = create_activity(activity)
        if activity is None:
            return make_err_response("创建活动失败")
        
        # 构造响应数据
        result = {
            'id': activity.id,
            'name': activity.name,
            'status': activity.status
        }
        
        return make_succ_response(result)
    except ValueError as e:
        logger.error("创建活动参数错误: {}".format(e))
        return make_err_response("日期格式错误，请使用ISO格式", ResponseCode.PARAM_ERROR)
    except Exception as e:
        logger.error("创建活动失败: {}".format(e))
        return make_err_response("创建活动失败")


@activity_bp.route('/api/activities/<int:activity_id>', methods=['PUT'])
def update_activity_info(activity_id):
    """
    更新活动
    """
    try:
        # 获取请求参数
        params = request.get_json()
        
        # 查询活动
        activity = get_activity_by_id(activity_id)
        if activity is None:
            return make_err_response("活动不存在", ResponseCode.NOT_FOUND)
        
        # 更新活动信息
        if 'name' in params:
            activity.name = params.get('name')
        
        if 'description' in params:
            activity.description = params.get('description')
        
        if 'start_time' in params:
            activity.start_time = datetime.fromisoformat(params.get('start_time').replace('Z', '+00:00'))
        
        if 'end_time' in params:
            activity.end_time = datetime.fromisoformat(params.get('end_time').replace('Z', '+00:00'))
        
        if 'building_name' in params:
            activity.building_name = params.get('building_name')
        
        if 'building_address' in params:
            activity.building_address = params.get('building_address')
        
        if 'location' in params:
            activity.location = params.get('location')
        
        if 'cover_image' in params:
            activity.cover_image = params.get('cover_image')
        
        if 'access_password' in params:
            activity.access_password = params.get('access_password')
        
        # 自动更新活动状态
        update_activity_status(activity)
        
        # 保存活动
        activity = update_activity(activity)
        if activity is None:
            return make_err_response("更新活动失败")
        
        # 构造响应数据
        result = {
            'id': activity.id,
            'name': activity.name,
            'status': activity.status
        }
        
        return make_succ_response(result)
    except ValueError as e:
        logger.error("更新活动参数错误: {}".format(e))
        return make_err_response("日期格式错误，请使用ISO格式", ResponseCode.PARAM_ERROR)
    except Exception as e:
        logger.error("更新活动失败: {}".format(e))
        return make_err_response("更新活动失败")


@activity_bp.route('/api/activities/<int:activity_id>', methods=['DELETE'])
def delete_activity_by_id(activity_id):
    """
    删除活动
    """
    try:
        # 查询活动
        activity = get_activity_by_id(activity_id)
        if activity is None:
            return make_err_response("活动不存在", ResponseCode.NOT_FOUND)
        
        # 删除活动
        success = delete_activity(activity_id)
        if not success:
            return make_err_response("删除活动失败")
        
        return make_succ_response({"id": activity_id})
    except Exception as e:
        logger.error("删除活动失败: {}".format(e))
        return make_err_response("删除活动失败")
