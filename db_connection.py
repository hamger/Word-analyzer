#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql

# 连接数据库
def connect():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='words',
        charset='utf8mb4')
    return connection
