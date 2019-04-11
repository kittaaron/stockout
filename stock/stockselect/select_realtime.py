__author__ = 'kittaaron'
# 已选大单数据

import tushare as ts
from sqlalchemy import *
import config.logginconfig
import logging
from stock.stockselect.my_select import *
from model.HistData import HistData
from model.Fpya import Fpya
from stock.basic import *
from utils.SMSUtil import *
from utils.db_utils import *

session = getSession()

if __name__ == '__main__':
    codes = get_select_codes()
    select_map = get_all_select_map()
    stocks_map = get_stocks_map(get_by_codes(codes))
    attention_stocks = []
    recommend_stocks = []
    chicang_stocks = []
    now_year = datetime.date.today().year
    for code in codes:
        latest_hist = session.query(HistData).filter(and_(HistData.code == code)).order_by(desc(HistData.date)).first()
        stockinfo = stocks_map[code]
        stockinfo.current_price = latest_hist.close
        select_info = select_map[code]
        # 没有股息率，把最近的股息率拿出来推测股息率
        latest_fpya = session.query(Fpya).filter(Fpya.code == code).order_by(desc(Fpya.report_date)).first()
        if latest_fpya is not None:
            select_info.dividend_year = latest_fpya.year
            if int(now_year) - 1 == latest_fpya.year:
                ## 今年的分红
                select_info.dividend = round(latest_fpya.divi * 10 / float(latest_hist.close), 2)
            elif int(now_year) - 2 == latest_fpya.year:
                select_info.dividend = round(latest_fpya.divi * 10 * 10 / ((10 + latest_fpya.shares) * float(latest_hist.close)), 2)
            else:
                pass
            save_select(select_info)

        predict_net = select_info.predict_net
        if predict_net <= 0:
            logging.info("%s %s 缺少净利润数据.", code, stockinfo.name)
            continue
        # 单位万
        totals = stockinfo.totals * 10000
        eps = select_info.predict_net / totals
        safe_price = round(eps * select_info.safe_pe, 2)
        fair_price = round(eps * select_info.fair_pe, 2)
        select_info.safe_price = safe_price
        select_info.fair_price = fair_price
        real_pe = round(latest_hist.close / eps, 2)
        stockinfo.real_pe = real_pe
        if latest_hist.close <= float(safe_price):
            recommend_stocks.append(stockinfo)
        elif latest_hist.close <= float(safe_price) * 1.2:
            attention_stocks.append(stockinfo)
        logging.info("%s %s %s "
                     "安全pe: %s 安全价格: %s - "
                     "合理pe: %s 合理价格: %s - "
                     "当前pe: %s 当前价格: %s - "
                     "距安全线: %s, 距合理线: %s, 股息率(%s): %s",
                     code, stockinfo.name, latest_hist.date,
                     select_info.safe_pe, safe_price,
                     select_info.fair_pe, fair_price,
                     real_pe, latest_hist.close,
                     round((real_pe - select_info.safe_pe) / select_info.safe_pe, 2),
                     round((real_pe - select_info.fair_pe) / select_info.fair_pe, 2),
                     select_info.dividend_year, select_info.dividend)

    if len(attention_stocks) > 0 or len(recommend_stocks) > 0:
        attention_stock_names = ''
        attention_real_pes = ''
        recommend_stock_names = ''
        recommend_real_pes = ''
        for attention_stock in attention_stocks:
            attention_stock_names += attention_stock.name + ","
            attention_real_pes += str(attention_stock.real_pe) + ","
        for recommend_stock in recommend_stocks:
            recommend_stock_names += recommend_stock.name + ","
            recommend_real_pes += str(recommend_stock.real_pe) + ","
        recommend_params = [recommend_stock_names[:-1], recommend_real_pes[:-1], attention_stock_names, attention_real_pes]
        attention_params = [attention_stock_names[:-1], attention_real_pes[:-1]]
        if len(recommend_stocks) > 0:
            logging.info("到达安全价格(当前PE): %s", recommend_params)
            sendRecommendMsgTX(recommend_params)
        else:
            logging.info("接近安全价格(当前PE): %s", attention_params)
            sendAttentionMsgTX(attention_params)
    else:
        logging.info("没有需要注意的股票")