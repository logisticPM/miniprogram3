import json
from flask import Response

from wxcloudrun.constants import ResponseCode
from wxcloudrun.utils import CustomJSONEncoder


def make_succ_empty_response():
    """
    构造空数据成功响应
    :return: Response对象
    """
    data = json.dumps({'code': ResponseCode.SUCCESS, 'data': {}}, cls=CustomJSONEncoder)
    return Response(data, mimetype='application/json')


def make_succ_response(data):
    """
    构造带数据成功响应
    :param data: 响应数据
    :return: Response对象
    """
    data = json.dumps({'code': ResponseCode.SUCCESS, 'data': data}, cls=CustomJSONEncoder)
    return Response(data, mimetype='application/json')


def make_err_response(err_msg, code=ResponseCode.SYSTEM_ERROR):
    """
    构造错误响应
    :param err_msg: 错误信息
    :param code: 错误码
    :return: Response对象
    """
    data = json.dumps({'code': code, 'errorMsg': err_msg}, cls=CustomJSONEncoder)
    return Response(data, mimetype='application/json')
