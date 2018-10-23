# word-counter

A counter for show probability of each word's occurrence in the book.

## Usage
在`static`目录下放置你的pdf原文，在项目根目录下执行命令
```bash
python readpdf.py bookname
```
> `bookname` 只能由A-Z，a-z，0-9和_下划线组成

解析结果存放在数据库`words`下的名为`bookname`的表中。

## Changelog

### 2018.10.23

> 支持统计多本书

### 2018.10.21

> 添加页面置顶和置底功能

### 2018.10.21

> 接入数据库，实现列表查询和过滤指定单词的功能

### 2018.10.20

> 实现 pdf 文件解析
