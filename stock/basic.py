__author__ = 'kittaaron'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy import desc
import tushare as ts
from model.StockInfo import StockInfo
import logging
from config.dbconfig import getConfig
import config.logginconfig
from stock import idx

engine = create_engine(getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def add(stock, autocommit=True):
    session.add(stock)
    if autocommit:
        session.commit()


def get_industry_classified_dict():
    icdf = ts.get_industry_classified()
    industry_classified_dict = icdf.to_dict(orient='records')
    ret = {}
    for data in industry_classified_dict:
        ret[data['code']] = data['c_name']
    return ret


def get_concept_classified_dict():
    ccdf = ts.get_concept_classified()
    concept_classified_dict = ccdf.to_dict(orient='records')
    ret = {}
    for data in concept_classified_dict:
        ret[data['code']] = data['c_name']
    return ret


def get_today_all():
    df = ts.get_today_all()
    ret = {}
    for idx, serie in df.iterrows():
        ret[serie['code']] = serie['mktcap']
    return ret


def update_stock_basics():
    # get dataframe
    df = ts.get_stock_basics()

    stockDict = {}

    industry_classified_dict = get_industry_classified_dict()
    concept_classified_dict = get_concept_classified_dict()
    today_all = get_today_all()

    sz50s = idx.get_sz50s()
    zz500s = idx.get_zz500s()
    cnt = 0
    for index, row in df.iterrows():
        if row is None:
            logging.error("index: %s is null", index)
            continue
        stockDict[index] = row
        stock = session.query(StockInfo).filter_by(code=index).first()
        if stock is None:
            logging.info("code: %s not exist, new stock?", code)
            continue
        # 股票代码
        code = index
        # 股票名称
        name = row['name']
        # 股票行业
        stock.industry = str(row['industry'])
        if code in industry_classified_dict:
            stock.industry_classified = industry_classified_dict[code]
        if code in concept_classified_dict:
            stock.concept_classified = concept_classified_dict[code]
        if code in today_all:
            stock.mktcap = today_all[code]

        if code in sz50s:
            stock.issz50 = 1
        if code in zz500s:
            stock.zz500s = 1
        # 股票地区
        stock.area = str(row['area'])
        # 市盈率(市价P/盈利Earning比率)
        ## pe <= 0，一般是亏损的
        stock.pe = row['pe']
        # 市净率(市价P/Book value净资产)
        stock.pb = row['pb']
        # 流通股本(亿)
        stock.outstanding = row['outstanding']
        # 总股本(亿)
        stock.totals = row['totals']
        # 总资产(万)
        stock.totalAssets = row['totalAssets']
        # 流动资产
        stock.liquidAssets = row['liquidAssets']
        # 固定资产
        stock.fixedAssets = row['fixedAssets']
        # 资本公积???
        stock.reserved = row['reserved']
        # 每股
        stock.reservedPerShare = row['reservedPerShare']
        # 每股收益(Earnings Per Share)
        stock.esp = row['esp']
        # bvps 每股净资产
        stock.bvps = row['bvps']
        # 上市时间
        stock.timeToMarket = row['timeToMarket']
        # 未分配利润
        stock.undp = row['undp']
        # 每股未分配
        stock.perundp = row['perundp']
        # 收入同比(%)
        stock.rev = row['rev']
        # profit,利润同比(%)
        stock.profit = row['profit']
        # gpr,毛利率(%)
        stock.gpr = row['gpr']
        # 净利润率(%)
        stock.npr = row['npr']
        # 股东数量
        stock.holders = row['holders']
        cnt += 1
        # print(index)
        logging.info("start to save code: %s, idx: %d", stock.code, cnt)

        if stock.id == 1265:
            logging.info("1265: %s", str(stock))
        if stock.industry == 'nan' or stock.area == 'nan':
            stock.industry = ''
            stock.area = ''
            logging.info("outMarket? code: %s", stock.code)
            continue

        add(stock)


def query_stock_order_by_pe():
    records = session.query(StockInfo).filter(StockInfo.pe != 0.00).order_by(StockInfo.pe).all()
    for stock in records:
        logging.info("stock: %s", str(stock))


if __name__ == '__main__':
    update_stock_basics()
