# -*-coding: utf-8 -*-
# @Time    : 2024/4/28 10:26
# @Author  : ted
# @File    : utils.py
# @Software: PyCharm

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
