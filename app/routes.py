# -*-coding: utf-8 -*-
# @Time    : 2024/4/28 10:26
# @Author  : ted
# @File    : routes.py
# @Software: PyCharm

from flask import request, jsonify, abort
from flask_paginate import Pagination, get_page_args
from werkzeug.utils import secure_filename
from .models import db, UserInfo, Product
from .utils import allowed_file
import os


def get_users_paginated(page, per_page):
    # 从数据库查询并分页
    users_paginated = UserInfo.query.paginate(page=page, per_page=per_page, error_out=False)
    # 将查询结果转换为字典列表
    users_list = [user.to_dict() for user in users_paginated.items]
    return users_list, users_paginated.total

def configure_routes(app):

    @app.route('/receive_info', methods=['POST'])
    def receive_info():
        data = request.form
        email = data.get('Email')
        if not email:
            abort(400, 'Email is required.')

        user_info = UserInfo(
            name=data.get('Name'),
            email=email,
            country=data.get('Country'),
            client_type=data.get('Client_Type'),
            interested_vehicle=data.get('Interested_Vehicle'),
            comment=data.get('Comment')
        )
        db.session.add(user_info)
        db.session.commit()

        return jsonify(success=True), 201

    @app.route('/submit_product', methods=['POST'])
    def submit_product():
        # 假设前端以表单形式发送数据，包括文件和文本字段
        product_name = request.form.get('product_name')
        brand_name = request.form.get('brand_name')
        model = request.form.get('model')
        description_1 = request.form.get('description_1')
        description_2 = request.form.get('description_2')
        description_3 = request.form.get('description_3')
        # 查找数据库中是否已有该产品
        product = Product.query.filter_by(product_name=product_name).first()
        # 接收图片文件
        image_file = request.files.get('image')
        logo_file = request.files.get('logo')

        # 处理图片文件
        if image_file and allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)

        if logo_file and allowed_file(logo_file.filename):
            logo_filename = secure_filename(logo_file.filename)
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
            logo_file.save(logo_path)

        if product:
            # 如果产品已存在，更新信息
            product.brand_name = brand_name
            product.model = model
            product.description_1 = description_1
            product.description_2 = description_2
            product.description_3 = description_3
            product.image_path = image_path if image_path else product.image_path
            product.logo_path = logo_path if logo_path else product.logo_path
        # 创建产品记录
        else:
            product = Product(
            product_name=product_name,
            brand_name=brand_name,
            model=model,
            description_1=description_1,
            description_2=description_2,
            description_3=description_3,
            image_path=image_path if image_file and allowed_file(image_file.filename) else None,
            logo_path=logo_path if logo_file and allowed_file(logo_file.filename) else None
        )

            # 保存到数据库
            db.session.add(product)
        db.session.commit()

        return jsonify(product.to_dict()), 201

    @app.route('/get_info', methods=['GET'])
    def get_info():
        # 假设我们从数据库或文件系统中获取了数据列表
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        users, total = get_users_paginated(page, per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

        return jsonify({
            'data': users,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': list(pagination.pages)
            }
        })

    @app.route('/get_product_by_name', methods=['GET'])
    def get_product_by_name():
        product_name = request.args.get('product_name')
        if not product_name:
            return jsonify({'error': 'Product name is required'}), 400

        product = Product.query.filter_by(product_name=product_name).first()
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        return jsonify(product.to_dict())

    @app.route('/get_products', methods=['GET'])
    def get_products():
        # 可选地从查询参数获取返回的产品数量
        limit = request.args.get('limit', default=None, type=int)

        # 查询产品信息
        if limit:
            products = Product.query.limit(limit).all()
        else:
            products = Product.query.all()

        # 将产品列表转换为字典列表
        products_list = [product.to_dict() for product in products]

        return jsonify(products_list)
