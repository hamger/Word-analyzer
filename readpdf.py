#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import importlib
importlib.reload(sys)
import logging
# 获取logger实例
logger = logging.getLogger()
# 设置控制台只打印错误
logger.setLevel(logging.ERROR)
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import re
import json
import pymysql

# 你需要在当前文件的目录下运行改文件
path = './static/Tuesdays_with_Morrie.pdf'


def parse():
    # 以二进制读模式打开
    fb = open(path, 'rb')
    # 创建一个pdf文档分析器
    parser = PDFParser(fb)
    # 创建一个pdf文档对象
    doc = PDFDocument()

    # 连接分析器与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码
    # 如果没有密码，就创建一个空字符串
    doc.initialize()
    obj = {}
    amount = 0
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # pdf 资源管理器，来管理共享资源
        resource = PDFResourceManager()
        # 参数分析器
        laparam = LAParams()
        # 聚合器
        device = PDFPageAggregator(resource, laparams=laparam)
        # 创建PDF解释器
        interpreter = PDFPageInterpreter(resource, device)

        # 循环遍历列表，每次处理一个page的内容
        for index, page in enumerate(doc.get_pages()):  # doc.get_pages() 获取page列表
            # if index < 3:
            #     continue
            # if index == 4:
            #     break

            # 使用页面解释器来读取
            interpreter.process_page(page)
            # 使用聚合器获取内容
            layout = device.get_result()

            for out in layout:
                if hasattr(out, "get_text"):
                    # print(out.get_text())
                    # 去除无法识别的文字转化成的 (cid:12) 之类的代码
                    t = re.sub(r'\(cid:[\d]*\)', '', out.get_text())
                    # 去除特殊内容，如数字、's、'm、're、n't
                    tx = re.sub(r'(\d+|\'s|\'m|\'re|n\'t)', '', t)
                    # 去除标点符号，且将多个空格转化为一个空格
                    txt = re.sub(
                        r'[\s+\?\.\!\/_,`:;\-$%^*\[\]\{\})(+\"\']+|[+——！，。？、‘’“”~@#￥%……&*（）：]+', ' ', tx)
                    for word in txt.split():
                        # 将单词转化为小写
                        w = word.lower()
                        amount = amount + 1
                        if obj.__contains__(w):
                            obj[w] = obj[w] + 1
                        else:
                            obj[w] = 1
    # 连接数据库
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='test',
                                 charset='utf8mb4')

    # 清空 words 表，避免受前一次计算结果影响
    connection.cursor().execute('truncate table words')
    for key in obj:
        # 获取会话指针
        with connection.cursor() as cursor:
            # 创建一条sql语句
            sql = "REPLACE INTO words (word, count, probability) VALUES(%s, %s, %s)"
            # 执行sql语句
            cursor.execute(
                sql, (key, obj[key], round(obj[key] / amount * 10000, 2)))
            # 提交
            connection.commit()

    # 断开数据库连接
    connection.close()
    print("总词数: %s" % amount)
    # print('’' in obj)
    # print(json.dumps(obj, sort_keys=True, indent=4, separators=(',', ':')))


if __name__ == '__main__':
    parse()
