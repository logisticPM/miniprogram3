from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import config

# 因MySQLDB不支持Python3，使用pymysql扩展库代替MySQLDB库
pymysql.install_as_MySQLdb()

# 初始化web应用
app = Flask(__name__, instance_relative_config=True)
app.config['DEBUG'] = config.DEBUG

# 设定数据库链接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/flask_demo'.format(config.username, config.password,
                                                                             config.db_address)

# 初始化DB操作对象
db = SQLAlchemy(app)

# 加载控制器
from wxcloudrun import views

# 注册API蓝图
from wxcloudrun.controllers.activity_controller import activity_bp
from wxcloudrun.controllers.room_controller import room_bp
from wxcloudrun.controllers.room_type_controller import room_type_bp
from wxcloudrun.controllers.grab_controller import grab_bp
from wxcloudrun.controllers.user_controller import user_bp

app.register_blueprint(activity_bp)
app.register_blueprint(room_bp)
app.register_blueprint(room_type_bp)
app.register_blueprint(grab_bp)
app.register_blueprint(user_bp)

# 加载配置
app.config.from_object('config')
