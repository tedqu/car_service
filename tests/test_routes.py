# -*-coding: utf-8 -*-
# @Time    : 2024/4/28 10:28
# @Author  : ted
# @File    : test_routes.py
# @Software: PyCharm
import unittest
from flask import json
from app import create_app, db
from io import BytesIO
from app.models import UserInfo,Product
import logging

# 配置日志输出到控制台，级别为 INFO
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """在每个测试用例执行前运行，设置测试环境"""
        test_config = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'TESTING': True,
            # ...其他可能的测试配置项
        }


        self.app = create_app(test_config)
        # self.app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://sawyer:Welcome#1@mysql-car:3306/flask_db"
        self.app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///:memory:'
        # logging.info(f"sqliteURI:  {self.app.config['SQLALCHEMY_DATABASE_URI']}")

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """在每个测试用例执行后运行，清理环境"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_receive_info(self):
        """测试接收用户信息接口"""
        response = self.client.post('/receive_info', data={
            'Email': 'test@example.com',
            'Name': 'Test User'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue('success' in response.get_json())

    def test_submit_product(self):
        """测试提交产品接口"""
        data = {
            'product_name': 'Product 1',
            'brand_name': 'Brand 1',
            'model': 'Model 1',
            'description_1': 'Description 1',
            'description_2': 'Description 2',
            'description_3': 'Description 3',
            'image': (BytesIO(b'fake image data'), 'image.jpg'),
            'logo': (BytesIO(b'fake logo data'), 'logo.jpg')
        }

        # 发送 POST 请求
        response = self.client.post('/submit_product', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)
        # 检查数据库是否正确保存了数据
        product = Product.query.first()
        self.assertIsNotNone(product)
        self.assertEqual(product.product_name, 'Product 1')

        # 检查返回的 JSON 数据
        json_data = json.loads(response.data)
        self.assertEqual(json_data['product_name'], 'Product 1')

    def test_submit_product_update(self):
        """测试更新已存在产品的接口"""
        # 先创建一个产品
        original_product = Product(
            product_name='Existing Product',
            brand_name='Original Brand',
            model='Original Model'
        )
        db.session.add(original_product)
        db.session.commit()

        # 更新这个已存在的产品
        data = {
            'product_name': 'Existing Product',  # 使用同一个产品名称
            'brand_name': 'Updated Brand',
            'model': 'Updated Model',
            'description_1': 'Updated Description 1',
            'description_2': 'Updated Description 2',
            'description_3': 'Updated Description 3',
            'image': (BytesIO(b'fake updated image data'), 'updated_image.jpg'),
            'logo': (BytesIO(b'fake updated logo data'), 'updated_logo.jpg')
        }
        response = self.client.post('/submit_product', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)
        updated_product = Product.query.filter_by(product_name='Existing Product').first()
        self.assertEqual(updated_product.brand_name, 'Updated Brand')
        self.assertEqual(updated_product.model, 'Updated Model')

    def test_get_info(self):
        """测试获取信息分页接口"""
        # Set up test data
        for i in range(10):  # Add 10 user info entries
            user_info = UserInfo(
                name=f'Test User {i}',
                email=f'user{i}@example.com',
                country='Test Country',
                client_type='Test Type',
                interested_vehicle=f'Vehicle {i}',
                comment=f'Comment {i}'
            )
            db.session.add(user_info)
        db.session.commit()
        response = self.client.get('/get_info?page=1&per_page=5')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('data' in response.get_json())

    def test_get_products(self):
        """测试获取所有产品接口"""
        # 添加测试数据
        product1 = Product(product_name='Product 1', brand_name='Brand A', model='Model X')
        product2 = Product(product_name='Product 2', brand_name='Brand B', model='Model Y')
        db.session.add(product1)
        db.session.add(product2)
        db.session.commit()

        # 调用接口
        response = self.client.get('/get_products')
        self.assertEqual(response.status_code, 200)

        # 获取返回的数据
        products_list = response.get_json()

        # 确保返回的是一个列表
        self.assertIsInstance(products_list, list)

        # 检查返回的列表长度
        self.assertEqual(len(products_list), 2)

        # 检查返回的产品信息是否正确
        self.assertEqual(products_list[0]['product_name'], 'Product 1')
        self.assertEqual(products_list[1]['product_name'], 'Product 2')



if __name__ == '__main__':
    unittest.main()
