#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request, jsonify
import json

app = Flask(__name__)

from functools import wraps
from flask import make_response


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'


@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''


@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'


@app.route('/list', methods=['get'])
@allow_cross_domain
def getList():
    ddd = {
        'success': True,
        'strr': [12, 12, 4, 5, 6, 78, 11]
    }
    return jsonify(ddd)


if __name__ == '__main__':
    # 开启热更新
    app.debug = True
    # 指定 IP 和 端口
    app.run(host='127.0.0.1', port=5001)
