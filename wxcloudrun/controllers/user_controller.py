"""
用户管理控制器
"""
import logging
import hashlib
from flask import request, Blueprint

from wxcloudrun.model import User
from wxcloudrun.dao import (
    create_user, get_user_by_openid, update_user
)
from wxcloudrun.response import make_succ_response, make_err_response
from wxcloudrun.constants import ResponseCode

# 初始化日志
logger = logging.getLogger('log')

# 创建蓝图
user_bp = Blueprint('user', __name__)


@user_bp.route('/api/users/login', methods=['POST'])
def user_login():
    """
    用户登录/注册
    """
    try:
        # 获取请求参数
        params = request.get_json()
        
        # 参数校验
        if not params.get('openid'):
            return make_err_response("用户openid不能为空", ResponseCode.PARAM_ERROR)
        
        # 查询用户
        user = get_user_by_openid(params.get('openid'))
        
        # 如果用户不存在，则创建用户
        if user is None:
            user = User()
            user.openid = params.get('openid')
            user.nickname = params.get('nickname', '微信用户')
            user.avatar_url = params.get('avatar_url')
            user.is_admin = False
            
            # 保存用户
            user = create_user(user)
            if user is None:
                return make_err_response("创建用户失败")
        else:
            # 更新用户信息
            if 'nickname' in params:
                user.nickname = params.get('nickname')
            
            if 'avatar_url' in params:
                user.avatar_url = params.get('avatar_url')
            
            # 保存用户
            user = update_user(user)
            if user is None:
                return make_err_response("更新用户信息失败")
        
        # 构造响应数据
        result = {
            'id': user.id,
            'openid': user.openid,
            'nickname': user.nickname,
            'avatar_url': user.avatar_url,
            'is_admin': user.is_admin
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("用户登录失败: {}".format(e))
        return make_err_response("用户登录失败")


@user_bp.route('/api/users/admin_login', methods=['POST'])
def admin_login():
    """
    管理员登录
    """
    try:
        # 获取请求参数
        params = request.get_json()
        
        # 参数校验
        if not params.get('openid'):
            return make_err_response("用户openid不能为空", ResponseCode.PARAM_ERROR)
        
        if not params.get('password'):
            return make_err_response("密码不能为空", ResponseCode.PARAM_ERROR)
        
        # 查询用户
        user = get_user_by_openid(params.get('openid'))
        if user is None:
            return make_err_response("用户不存在", ResponseCode.NOT_FOUND)
        
        # 验证密码
        # 注意：这里应该使用更安全的密码验证方式，例如bcrypt
        # 此处仅为示例，实际应用中应使用更安全的方式
        admin_password = "admin123"  # 实际应用中应从配置文件或环境变量中获取
        hashed_password = hashlib.md5(admin_password.encode()).hexdigest()
        input_password = hashlib.md5(params.get('password').encode()).hexdigest()
        
        if input_password != hashed_password:
            return make_err_response("密码错误", ResponseCode.FORBIDDEN)
        
        # 设置为管理员
        user.is_admin = True
        
        # 保存用户
        user = update_user(user)
        if user is None:
            return make_err_response("更新用户信息失败")
        
        # 构造响应数据
        result = {
            'id': user.id,
            'openid': user.openid,
            'nickname': user.nickname,
            'avatar_url': user.avatar_url,
            'is_admin': user.is_admin
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("管理员登录失败: {}".format(e))
        return make_err_response("管理员登录失败")


@user_bp.route('/api/users/profile', methods=['GET'])
def get_user_profile():
    """
    获取用户信息
    """
    try:
        # 获取查询参数
        openid = request.args.get('openid')
        
        # 参数校验
        if not openid:
            return make_err_response("用户openid不能为空", ResponseCode.PARAM_ERROR)
        
        # 查询用户
        user = get_user_by_openid(openid)
        if user is None:
            return make_err_response("用户不存在", ResponseCode.NOT_FOUND)
        
        # 构造响应数据
        result = {
            'id': user.id,
            'openid': user.openid,
            'nickname': user.nickname,
            'avatar_url': user.avatar_url,
            'is_admin': user.is_admin,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error("获取用户信息失败: {}".format(e))
        return make_err_response("获取用户信息失败")
