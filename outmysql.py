# -*- coding:utf-8 -*-
# Author: kittaaron

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tushare as ts
import pymysql
import logging
import logging.config
import time
import datetime
from model import StockInfo

from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

def dumpHiDateRangeData(code, startDateStr, endDateStr):
    startDate = datetime.datetime.strptime(startDateStr, '%Y-%m-%d')
    if code in stockDict:
        timeToMarket = stockDict[code]['timeToMarket']
        if timeToMarket > 0:
            timeToMarketDate = datetime.datetime.strptime(str(timeToMarket), '%Y%m%d')
            if startDate < timeToMarketDate:
                logging.info("timeToMarketDate: %s", timeToMarketDate)
                startDate = timeToMarketDate
    endDate = datetime.datetime.strptime(endDateStr, '%Y-%m-%d')
    logging.info("code: %s, startDate: %s, endDate: %s", code, startDate, endDate)
    while startDate <= endDate:
        try:
            tmpDateStr = startDate.strftime('%Y-%m-%d')
            startDate += datetime.timedelta(days = 1)
            #dumpHiDateData(code, tmpDateStr)
            #time.sleep(time.sleep(random.randint(1,3)))
        except Exception as e:
            logging.error("dum error, code: %s, date: %s", code, tmpDateStr)

## dum数据到mysql
def dumpHiDateData(code, dateStr):
    logging.info("start dump code : %s , date: %s", code, dateStr)
    df = ts.get_tick_data(code, date=dateStr)
    df.to_sql('tick_data',engine, if_exists='append')

## 获取所有上证股票代码
def getAllSSECCodes():
    return getStockCodesBySql("select code from stockinfo where code like '60%'")

## 获取所有深证股票代码
def getAllSZSECodes():
    return getStockCodesBySql("select code from stockinfo where code like '00%'")

## 获取创业版所有股票代码
def getCYBCodes():
    return getStockCodesBySql("select code from stockinfo where code like '300%'")

def getStockCodesBySql(sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    codes = []
    for row in results:
        code = row[0]
        codes.append(code)
    return codes

def dumpSSECHiData(startDateStr, endDateStr):
    ssecCodes = getAllSSECCodes()
    for code in ssecCodes:
        dumpHiDateRangeData(code, startDateStr, endDateStr)

    szseCodes = getAllSZSECodes()
    for code in szseCodes:
        dumpHiDateRangeData(code, startDateStr, endDateStr)

    cybCodes = getCYBCodes()
    for code in cybCodes:
        dumpHiDateRangeData(code, startDateStr, endDateStr)

#追加数据到现有表
#df.to_sql('tick_data',engine,if_exists='append')

if __name__ == '__main__':
    startDateStr = '2008-01-01'
    today = str(datetime.date.today())
    logging.info("start: %s, end: %s", startDateStr, today)
    #dumpSSECHiData(startDateStr, today)

