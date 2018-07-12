# -*- coding:utf-8 -*-
# Author: kittaaron

import urllib
import urllib.request
import re
import sys
import importlib
import pymysql

def insertCodeInfo(db, cursor, code, name):
    sql = "insert into stockinfo(code, name) values('" + str(code) + "','" + str(name) + "')";
    try:
        print(sql)
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        exit(0)
        # 如果发生错误则回滚
        db.rollback()

response = urllib.request.urlopen('http://quote.eastmoney.com/stocklist.html')
content = response.read().decode("gbk")
pattern = re.compile('<li><a.*?href=.*?html">(.*?)</a></li>', re.S)
items = re.findall(pattern,content)

importlib.reload(sys)
#f = open('stocklist.txt','w')

db = pymysql.connect("127.0.0.1","root","123456","stockout" )
cursor = db.cursor()

getcodePattern = re.compile('(.*)\((.*)\)', re.S)
for item in items:
    matched = re.findall(getcodePattern, item)
    name = matched[0][0]
    code = matched[0][1]
    insertCodeInfo(db, cursor, code, name)
#f.close()

db.close()
