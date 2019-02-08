__author__ = 'kittaaron'
# 已选大单数据

import tushare as ts
from sqlalchemy import *
import config.logginconfig
import logging
from stock.stockselect.my_select import *
from model.HistData import HistData
from stock.basic import *
from utils.SMSUtil import *


if __name__ == '__main__':
    codes = get_select_codes()
    select_map = get_all_select_map()
    stocks_map = get_stocks_map(get_by_codes(codes))
    for code in codes:
        latest_hist = session.query(HistData).filter(and_(HistData.code == code)).order_by(desc(HistData.date)).first()
        stockinfo = stocks_map[code]
        select_info = select_map[code]
        predict_net = select_info.predict_net
        if predict_net <= 0:
            logging.info("%s %s 缺少净利润数据.", code, stockinfo.name)
            continue
        # 单位万
        totals = stockinfo.totals * 10000
        eps = select_info.predict_net / totals
        real_pe = round(latest_hist.close / eps, 2)
        logging.info("%s %s %s 安全pe: %s 合理pe: %s 实际pe: %s, 距离安全线: %s", code, stockinfo.name,
                     latest_hist.date, select_info.safe_pe, select_info.fair_pe, real_pe,
                     round((real_pe - select_info.safe_pe) / select_info.safe_pe, 2))