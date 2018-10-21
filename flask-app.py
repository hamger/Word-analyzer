#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request, jsonify
import json
import pymysql

app = Flask(__name__)

from functools import wraps
from flask import make_response


# 连接数据库
def connect():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='test',
        charset='utf8mb4')
    return connection


# 规定接口的数据返回格式
def baseReturn(data='', msg='OK', success=True):
    json_data = json.dumps({'data': data, 'success': success, 'msg': msg})
    return json_data


# 允许跨域访问
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


@app.route('/list2', methods=['get'])
@allow_cross_domain
def getList2():
    print(request.get_data())
    db = connect()
    cursor = db.cursor()
    cursor.execute(
        'select * from words where probability > 100 ORDER BY probability DESC'
    )
    data = cursor.fetchall()
    db.close()
    return baseReturn(data)


# 添加我掌握的单词
@app.route('/addMyWord', methods=['post'])
@allow_cross_domain
def addMyWord():
    words = json.loads(request.get_data())
    db = connect()
    for word in words:
        # 获取会话指针
        with db.cursor() as cursor:
            # 创建一条 sql 语句，如果表名或字段名中带 - ，需要使用 ` 包裹
            sql = "REPLACE INTO `my-words` (word) VALUES(%s)"
            # 执行sql语句
            cursor.execute(sql, (word))
            # 提交
            db.commit()
    db.close()
    return baseReturn('', '加入成功')


if __name__ == '__main__':
    # 开启热更新
    app.debug = True
    # 指定 IP 和 端口
    app.run(host='127.0.0.1', port=5001)
