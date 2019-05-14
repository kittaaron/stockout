__author__ = 'kittaaron'

import tushare as ts
from model.StockInfo import StockInfo
import logging
from config.dbconfig import getConfig
import config.logginconfig
from stock import idx
from utils.db_utils import *
from pypinyin import pinyin, lazy_pinyin, Style
from utils.pinyin_util import *

session = Session()


def get_by_code(code):
    try:
        return session.query(StockInfo).filter(StockInfo.code == code).first()
    except Exception as e:
        pass
    finally:
        session.close()


def get_by_name(name):
    try:
        return session.query(StockInfo).filter(StockInfo.name.in_(name)).first()
    except Exception as e:
        pass
    finally:
        session.close()


def get_by_code_like(param):
    try:
        return session.query(StockInfo).filter(StockInfo.code.like(param + '%')).limit(10).all()
    except Exception as e:
        pass
    finally:
        session.close()


def get_by_abbr_like(param):
    try:
        # 缩写like
        param += "%"
        return session.query(StockInfo).filter(StockInfo.abbr.like(param)).limit(10).all()
    except Exception as e:
        pass
    finally:
        session.close()


def get_by_codes(codes):
    try:
        return session.query(StockInfo).filter(StockInfo.code.in_(codes)).all()
    except Exception as e:
        pass
    finally:
        session.close()


def get_by_names(names):
    try:
        return session.query(StockInfo).filter(StockInfo.name.in_(names)).all()
    except Exception as e:
        pass
    finally:
        session.close()


def get_codes_by_names(names):
    try:
        stocks = session.query(StockInfo).filter(StockInfo.name.in_(names)).all()
        codes = []
        for stock in stocks:
            codes.append(stock.code)
        return codes
    except Exception as e:
        pass
    finally:
        session.close()


def get_all_stocks():
    try:
        stocks = session.query(StockInfo).all()
        return stocks
    except Exception as e:
        pass
    finally:
        session.close()


def get_stocks_map(stocks):
    try:
        ret = {}
        for stock in stocks:
            ret[stock.code] = stock
        return ret
    except Exception as e:
        pass
    finally:
        session.close()


def get_all_codes():
    try:
        codes = []
        stocks = get_all_stocks()
        for stock in stocks:
            codes.append(stock.code)
        return codes
    except Exception as e:
        pass
    finally:
        session.close()


def get_all_stocks_map():
    try:
        ret = {}
        stocks = get_all_stocks()
        for stock in stocks:
            ret[stock.code] = stock
        return ret
    except Exception as e:
        pass
    finally:
        session.close()


def get_industry_classified_dict():
    try:
        icdf = ts.get_industry_classified()
        industry_classified_dict = icdf.to_dict(orient='records')
        ret = {}
        for data in industry_classified_dict:
            ret[data['code']] = data['c_name']
        return ret
    except Exception as e:
        pass
    finally:
        session.close()


def get_concept_classified_dict():
    try:
        ccdf = ts.get_concept_classified()
        concept_classified_dict = ccdf.to_dict(orient='records')
        ret = {}
        for data in concept_classified_dict:
            ret[data['code']] = data['c_name']
        return ret
    except Exception as e:
        pass
    finally:
        session.close()


def get_today_all():
    try:
        df = ts.get_today_all()
        ret = {}
        for idx, serie in df.iterrows():
            ret[serie['code']] = serie['mktcap']
        return ret
    except Exception as e:
        pass
    finally:
        session.close()


def update_stock_basics():
    try:
        # get dataframe
        df = ts.get_stock_basics()

        industry_classified_dict = get_industry_classified_dict()
        concept_classified_dict = get_concept_classified_dict()
        today_all = get_today_all()

        sz50s = idx.get_sz50s()
        zz500s = idx.get_zz500s()
        cnt = 0
        stocks_to_save = []
        for index, row in df.iterrows():
            if index is None or row is None:
                logging.error("wrong data. index: %s, row: %s", index, row)
                continue
            # 股票代码
            code = index
            # 股票名称
            name = row['name']
            if name.startswith('ST') or name.startswith('*ST') or name.startswith('**ST'):
                abbr = 'st' + get_acronym(name[name.index('T')+1:])
            else:
                abbr = get_acronym(name)
            stock = session.query(StockInfo).filter_by(code=index).first()
            if stock is None:
                logging.info("%s %s not exist, new stock?", code, name)
                stock = StockInfo()
            stock.code = code
            stock.name = name
            stock.abbr = abbr.replace(' ', '')
            # 股票行业
            stock.industry = str(row['industry'])
            if code in industry_classified_dict:
                stock.industry_classified = industry_classified_dict[code]
            if code in concept_classified_dict:
                stock.concept_classified = concept_classified_dict[code]
            if code in today_all and today_all[code] is not None:
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
            logging.info("start to save  %s %s, idx: %d", code, name, cnt)

            if stock.industry == 'nan' or stock.area == 'nan':
                stock.industry = ''
                stock.area = ''
                logging.info("已退市? %s %s", code, name)
                continue

            session.add(stock)
    except Exception as e:
        pass
    finally:
        session.close()


def query_stock_order_by_pe():
    try:
        records = session.query(StockInfo).filter(StockInfo.pe != 0.00).order_by(StockInfo.pe).all()
        for stock in records:
            logging.info("stock: %s %s", stock.code, stock.name)
    except Exception as e:
        pass
    finally:
        session.close()


if __name__ == '__main__':
    update_stock_basics()
