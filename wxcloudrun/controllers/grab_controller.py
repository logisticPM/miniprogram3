"""
抢购记录管理控制器
"""
import logging
from flask import request, Blueprint

from wxcloudrun.dao import (
    get_grab_record_by_id, get_grab_records_by_user, update_grab_record,
    get_room_by_id, update_room, get_user_by_openid
)
from wxcloudrun.response import make_succ_response, make_err_response
from wxcloudrun.constants import ResponseCode, GrabStatus, RoomStatus

# 初始化日志
logger = logging.getLogger('log')

# 创建蓝图
grab_bp = Blueprint('grab', __name__)


@grab_bp.route('/api/grabs', methods=['GET'])
def list_grab_records():
    """
    获取用户抢购记录列表
    """
    try:
        # 获取查询参数
        openid = request.args.get('openid')
        status = request.args.get('status')
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        
        # 参数校验
        if not openid:
            return make_err_response("用户openid不能为空", ResponseCode.PARAM_ERROR)
        
        # 获取用户
        user = get_user_by_openid(openid)
        if user is None:
            return make_err_response("用户不存在", ResponseCode.NOT_FOUND)
        
        # 查询抢购记录列表
        grab_records = get_grab_records_by_user(user.id, status, limit, offset)
        
        # 构造响应数据
        result = []
        for record in grab_records:
            # 获取房间信息
            room = get_room_by_id(record.room_id)
            room_info = None
            if room:
                room_info = {
                    'id': room.id,
                    'room_number': room.room_number,
                    'floor': room.floor,
                    'orientation': room.orientation,
                    'actual_price': float(room.actual_price),
                    'status': room.status,
                    'image_urls': room.image_urls
                }
            
            # 添加记录信息
            result.append({
                'id': record.id,
                'user_id': record.user_id,
                'room_id': record.room_id,
                'status': record.status,
                'grab_time': record.grab_time,
                'confirm_time': record.confirm_time,
                'notes': record.notes,
                'room': room_info
            })
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("获取抢购记录列表失败: {}".format(e))
        return make_err_response("获取抢购记录列表失败")


@grab_bp.route('/api/grabs/<int:grab_id>', methods=['GET'])
def get_grab_record(grab_id):
    """
    获取抢购记录详情
    """
    try:
        # 查询抢购记录
        grab_record = get_grab_record_by_id(grab_id)
        if grab_record is None:
            return make_err_response("抢购记录不存在", ResponseCode.NOT_FOUND)
        
        # 获取房间信息
        room = get_room_by_id(grab_record.room_id)
        room_info = None
        if room:
            room_info = {
                'id': room.id,
                'room_number': room.room_number,
                'floor': room.floor,
                'orientation': room.orientation,
                'actual_price': float(room.actual_price),
                'status': room.status,
                'image_urls': room.image_urls
            }
        
        # 构造响应数据
        result = {
            'id': grab_record.id,
            'user_id': grab_record.user_id,
            'room_id': grab_record.room_id,
            'status': grab_record.status,
            'grab_time': grab_record.grab_time,
            'confirm_time': grab_record.confirm_time,
            'notes': grab_record.notes,
            'room': room_info
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("获取抢购记录详情失败: {}".format(e))
        return make_err_response("获取抢购记录详情失败")


@grab_bp.route('/api/grabs/<int:grab_id>/confirm', methods=['POST'])
def confirm_grab(grab_id):
    """
    确认购买
    """
    try:
        # 获取请求参数
        params = request.get_json()
        
        # 参数校验
        if not params.get('openid'):
            return make_err_response("用户openid不能为空", ResponseCode.PARAM_ERROR)
        
        # 查询抢购记录
        grab_record = get_grab_record_by_id(grab_id)
        if grab_record is None:
            return make_err_response("抢购记录不存在", ResponseCode.NOT_FOUND)
        
        # 获取用户
        user = get_user_by_openid(params.get('openid'))
        if user is None:
            return make_err_response("用户不存在", ResponseCode.NOT_FOUND)
        
        # 检查用户权限
        if grab_record.user_id != user.id:
            return make_err_response("无权操作此抢购记录", ResponseCode.FORBIDDEN)
        
        # 检查抢购记录状态
        if grab_record.status != GrabStatus.PENDING:
            return make_err_response("抢购记录状态不允许确认购买", ResponseCode.BUSINESS_ERROR)
        
        # 获取房间
        room = get_room_by_id(grab_record.room_id)
        if room is None:
            return make_err_response("房间不存在", ResponseCode.NOT_FOUND)
        
        # 更新抢购记录状态
        grab_record.status = GrabStatus.CONFIRMED
        grab_record = update_grab_record(grab_record)
        if grab_record is None:
            return make_err_response("更新抢购记录状态失败")
        
        # 更新房间状态
        room.status = RoomStatus.SOLD
        room = update_room(room)
        if room is None:
            return make_err_response("更新房间状态失败")
        
        # 构造响应数据
        result = {
            'id': grab_record.id,
            'status': grab_record.status,
            'confirm_time': grab_record.confirm_time
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("确认购买失败: {}".format(e))
        return make_err_response("确认购买失败")


@grab_bp.route('/api/grabs/<int:grab_id>/cancel', methods=['POST'])
def cancel_grab(grab_id):
    """
    取消抢购
    """
    try:
        # 获取请求参数
        params = request.get_json()
        
        # 参数校验
        if not params.get('openid'):
            return make_err_response("用户openid不能为空", ResponseCode.PARAM_ERROR)
        
        # 查询抢购记录
        grab_record = get_grab_record_by_id(grab_id)
        if grab_record is None:
            return make_err_response("抢购记录不存在", ResponseCode.NOT_FOUND)
        
        # 获取用户
        user = get_user_by_openid(params.get('openid'))
        if user is None:
            return make_err_response("用户不存在", ResponseCode.NOT_FOUND)
        
        # 检查用户权限
        if grab_record.user_id != user.id and not user.is_admin:
            return make_err_response("无权操作此抢购记录", ResponseCode.FORBIDDEN)
        
        # 检查抢购记录状态
        if grab_record.status != GrabStatus.PENDING:
            return make_err_response("抢购记录状态不允许取消", ResponseCode.BUSINESS_ERROR)
        
        # 获取房间
        room = get_room_by_id(grab_record.room_id)
        if room is None:
            return make_err_response("房间不存在", ResponseCode.NOT_FOUND)
        
        # 更新抢购记录状态
        grab_record.status = GrabStatus.CANCELLED
        grab_record = update_grab_record(grab_record)
        if grab_record is None:
            return make_err_response("更新抢购记录状态失败")
        
        # 更新房间状态
        room.status = RoomStatus.AVAILABLE
        room = update_room(room)
        if room is None:
            return make_err_response("更新房间状态失败")
        
        # 构造响应数据
        result = {
            'id': grab_record.id,
            'status': grab_record.status
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("取消抢购失败: {}".format(e))
        return make_err_response("取消抢购失败")
