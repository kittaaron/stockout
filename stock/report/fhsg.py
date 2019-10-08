"""
分红送股数据
"""
from utils.db_utils import *
from model.StockInfo import StockInfo
from model.report.Fhsg import Fhsg
import tushare as ts
import config.logginconfig
import logging
import math
import time
from sqlalchemy import *
import traceback

session = getSession()
pro = ts.pro_api('c4ccc5b28a49ae5f7b82d84d0d28bbc366d6f50f16bcb3cf21ae3d43')


def dump_fhsg(code, name, row):
    """
        dump分红送股数据
    :param code:
    :param name:
    :param row:
    :return:
    """
    try:
        fhsgs = session.query(Fhsg).filter(Fhsg.code ==  code).delete()
        param_code = code + '.SH' if code.startswith('6') else code + '.SZ'

        df = pro.dividend(ts_code=param_code, fields='ts_code,div_proc,end_date,ann_date,stk_div,cash_div,cash_div_tax,record_date,ex_date,base_share,base_date')

        if df.empty:
            logging.info("%s %s 分红送股数据为空", code, name)
            return
        datas = []
        for index, serie in df.iterrows():
            if 'base_share' not in serie or math.isnan(serie['base_share']) or 'cash_div' not in serie:
                continue
            if 'record_date' not in serie or serie['record_date'] is None  or 'ex_date' not in serie or serie['ex_date'] is None:
                continue
            fhsg = Fhsg(code, name)
            # 分红年份
            fhsg.end_date = serie['end_date']
            fhsg.ann_date = serie['ann_date']
            fhsg.stk_div = serie['stk_div']
            #fhsg.stk_bo_rate = serie['stk_bo_rate']
            #fhsg.stk_co_rate = serie['stk_co_rate']
            fhsg.cash_div = serie['cash_div']
            fhsg.cash_div_tax = serie['cash_div_tax']
            fhsg.record_date = serie['record_date']
            fhsg.ex_date = serie['ex_date']
            #fhsg.pay_date = serie['pay_date']
            #fhsg.div_listdate = serie['div_listdate']
            #fhsg.imp_ann_date = serie['imp_ann_date']
            #fhsg.base_date = serie['base_date']
            # 基准股本
            fhsg.base_share = serie['base_share']
            datas.append(fhsg)

        session.add_all(datas)
        session.commit()
        logging.info("%s %s 保存成功", code, name)
    except Exception as e:
        traceback.print_exc()
    finally:
        session.close()

def get_ordered_fhrate(search_date, page, page_size):
    try:
        offset = page * page_size
        ret = session.query(Fhsg).filter(and_(Fhsg.end_date == search_date, Fhsg.cash_rate > 0)).order_by(desc(Fhsg.cash_rate)).limit(page_size).offset(offset).all()
        return ret
    except Exception as e:
        traceback.print_exc()
    finally:
        session.close()

if __name__ == '__main__':
    stocks = session.query(StockInfo).all()
    #stocks = session.query(StockInfo).filter(StockInfo.code == '601636').all()
    i = 0
    for row in stocks:
        if row is None:
            continue
        code = row.code
        name = row.name
        dump_fhsg(code, name, row)
        i+=1
        if i % 98 == 0:
            time.sleep(45)