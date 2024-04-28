# -*-coding: utf-8 -*-
# @Time    : 2024/4/28 10:39
# @Author  : ted
# @File    : models.py
# @Software: PyCharm


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))
    client_type = db.Column(db.String(100))
    interested_vehicle = db.Column(db.String(100))
    comment = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'country': self.country,
            'client_type': self.client_type,
            'interested_vehicle': self.interested_vehicle,
            'comment': self.comment
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(120), nullable=False)  # 产品名称
    image_path = db.Column(db.String(120), nullable=True)  # 产品图片路径
    logo_path = db.Column(db.String(120), nullable=True)  # 品牌logo路径
    brand_name = db.Column(db.String(120), nullable=False)  # 品牌名称
    model = db.Column(db.String(120))  # 车型
    description_1 = db.Column(db.Text, nullable=True)  # 描述一
    description_2 = db.Column(db.Text, nullable=True)  # 描述二
    description_3 = db.Column(db.Text, nullable=True)  # 描述三

    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'image_path': self.image_path,
            'logo_path': self.logo_path,
            'brand_name': self.brand_name,
            'model': self.model,
            'description_1': self.description_1,
            'description_2': self.description_2,
            'description_3': self.description_3,
        }


