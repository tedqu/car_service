# -*-coding: utf-8 -*-
# @Time    : 2024/4/28 10:21
# @Author  : ted
# @File    : __init__.py
# @Software: PyCharm

from flask import Flask
from .models import db
import os
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is not None:
        # 加载测试配置
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
            'mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@mysql-car/${MYSQL_DATABASE}'
    logging.info(f"database_url:  {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.config['UPLOAD_FOLDER'] = './images'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()  # 创建数据库表

    from .routes import configure_routes
    configure_routes(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app

