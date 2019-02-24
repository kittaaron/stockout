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
from utils.db_utils import *


if __name__ == '__main__':
    codes = get_select_codes()
    select_map = get_all_select_map()
    stocks_map = get_stocks_map(get_by_codes(codes))
    for code in codes:
        latest_hist = getSession().query(HistData).filter(and_(HistData.code == code)).order_by(desc(HistData.date)).first()
        stockinfo = stocks_map[code]
        select_info = select_map[code]
        predict_net = select_info.predict_net
        if predict_net <= 0:
            logging.info("%s %s 缺少净利润数据.", code, stockinfo.name)
            continue
        # 单位万
        totals = stockinfo.totals * 10000
        eps = select_info.predict_net / totals
        safe_price = round(eps * select_info.safe_pe, 2)
        fair_price = round(eps * select_info.fair_pe, 2)
        real_pe = round(latest_hist.close / eps, 2)
        logging.info("%s %s %s "
                     "安全pe: %s 安全价格: %s - "
                     "合理pe: %s 合理价格: %s - "
                     "当前pe: %s 当前价格: %s - "
                     "距安全线: %s, 距合理线: %s",
                     code, stockinfo.name, latest_hist.date,
                     select_info.safe_pe, safe_price,
                     select_info.fair_pe, fair_price,
                     real_pe, latest_hist.close,
                     round((real_pe - select_info.safe_pe) / select_info.safe_pe, 2),
                     round((real_pe - select_info.fair_pe) / select_info.fair_pe, 2))