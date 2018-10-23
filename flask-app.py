#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request, jsonify
import json
import pymysql

app = Flask(__name__)

from functools import wraps
from flask import make_response
from html_downloader import download
from html_parser import prase


# 爬取数据
def carw(url):
    html_cont = download(url)
    return prase(html_cont)


# 连接数据库
def connect():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='words',
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


# 查询所有书名的列表
@app.route('/book', methods=['get'])
@allow_cross_domain
def getbook():
    db = connect()
    cursor = db.cursor()
    sql = "select table_name from information_schema.tables where table_schema='words'"
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    list = []
    for x in data:
        if not str(x[0]) == 'my_words':
            list.append(str(x[0]))
    return baseReturn(list)


# 列表查询
@app.route('/list', methods=['get'])
@allow_cross_domain
def getList():
    bookName = request.args.get('bookName')
    proFrom = request.args.get('proFrom')
    proTo = request.args.get('proTo')
    if proFrom == None:
        proFrom = 0
    if proTo == None:
        proTo = 10000
    db = connect()
    cursor = db.cursor()
    # 获取 过滤掉 my_words 表中的单词，且指定出现概率范围下的，倒序排列的数据
    sql = 'select * from ' + bookName + ' where (select count(1) as num from my_words where my_words.word =' + bookName + '.word) = 0 and probability >= %s and probability <= %s ORDER BY probability DESC'

    cursor.execute(sql,
                   (request.args.get('proFrom'), request.args.get('proTo')))
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
            sql = "REPLACE INTO my_words (word) VALUES(%s)"
            # 执行sql语句
            cursor.execute(sql, (word))
            # 提交
            db.commit()
    db.close()
    return baseReturn('', '加入成功')


# 查询单词
@app.route('/checkWord', methods=['get'])
@allow_cross_domain
def checkWord():
    word = request.args.get('word')
    url = 'http://dict.youdao.com/search?q=' + word
    data = carw(url)
    return baseReturn(data, '查询成功')


if __name__ == '__main__':
    # 开启热更新
    app.debug = True
    # 指定 IP 和 端口
    app.run(host='127.0.0.1', port=5001)
