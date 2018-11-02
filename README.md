# word-counter

一个用来统计英文原著中每个单词出现概率的工具。

## Purpose

阅读英文原著可以大大提高语感和词汇量，但是我们常常没有勇气去看，担心以自己的词汇量，没看几句就要去查词典了，很是痛苦。为了解决这个问题，苦思冥想后我打算做一个词汇统计器，word-counter 就这样诞生了。它可以统计一本英文原著中所有单词出现的概率，初始提供一个词汇量 1900 的过滤本去过滤基础的单词，剩下的你可以根据自己的水平将某些单词加入过滤本，最后展现出来的就是你的生词了，努力背几遍这些单词，然后带着记忆去阅读，你会发现其实你是能看懂英文原著的（可以先从儿童文学开始试试），慢慢地词汇量就会提高。

## Usage

#### 导入数据库

将`words_1900.sql`导入 mysql 数据库，将`db_connection.py`中的数据库连接配置项修改成你的配置，输入以下命令行开启 mysql ：

```bash
mysql.server start
```

#### 解析 pdf

在`static`目录下放置你的 pdf 原文，在项目根目录下执行命令

```bash
python readpdf.py bookName
```

> `bookName` 只能由 A-Z，a-z，0-9 和\_下划线组成

终端返回本书的总词数时说明统计结束

#### 启动服务

在项目根目录下执行命令

```bash
python flask_app.py
```

打开`index.html`即可查看和管理统计结果。

## Changelog

### 2018.11.2

> 支持快速查词

### 2018.10.24

> 支持过滤列表的管理

### 2018.10.23

> 支持统计多本书

### 2018.10.21

> 添加页面置顶和置底功能

### 2018.10.21

> 接入数据库，实现列表查询和过滤指定单词的功能

### 2018.10.20

> 实现 pdf 文件解析
