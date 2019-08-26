from typing import Any, Union

import tushare as ts
import logging
import config.logginconfig
from stock.report.report_utils import *
from sqlalchemy.orm import aliased
from utils.db_utils import *
from model.report.Zycwzb import Zycwzb
from model.report.Zcfzb import Zcfzb
from sqlalchemy import *
from model.StockInfo import StockInfo
from model.RealTimePEEPS import RealTimePEEPS
from stock.report.report_utils import *
from numpy import *
from model.Buffett import Buffett
from model.RealTimePB import RealTimePB
from model.HistData import HistData
import traceback


session = getSession()


def get_codes(stocks):
    codes = []
    for stock in stocks:
        codes.append(stock.code)
    return codes


def build_map(realtimepeeps):
    ret = {}
    for realtimepeeps in realtimepeeps:
        ret[realtimepeeps.code] = realtimepeeps
    return ret

def get_stocks_map(stocks):
    ret = {}
    for stock in stocks:
        ret[stock.code] = stock
    return ret


def get_buffetts_map(buffetts):
    ret = {}
    for buffett in buffetts:
        ret[buffett.code] = buffett
    return ret


def get_pe_ranking_datas(page, pageSize):
    try:
        """
            获取根据pe排名的股票数据
        :return:
        """
        page = 0 if not page else page
        pageSize = 200 if not pageSize else pageSize
        offset = page * pageSize
        realtime_pe_eps = session.query(RealTimePEEPS).filter(and_(RealTimePEEPS.koufei_pe > 0, RealTimePEEPS.pe1 > 0))\
            .order_by(RealTimePEEPS.koufei_pe).limit(pageSize).offset(offset).all()
        codes = get_codes(realtime_pe_eps)
        stocks = session.query(StockInfo).filter(StockInfo.code.in_(codes)).all()
        buffetts = session.query(Buffett).filter(Buffett.code.in_(codes)).all()
        codes_map = get_stocks_map(stocks)
        buffetts_map = get_buffetts_map(buffetts)
        ret = []
        for realtime_pe_ep in realtime_pe_eps:
            code = realtime_pe_ep.code
            if code in codes_map:
                realtime_pe_ep.industry = codes_map[realtime_pe_ep.code].industry
                realtime_pe_ep.industry_classified = codes_map[realtime_pe_ep.code].industry_classified
                realtime_pe_ep.mktcap = round(codes_map[realtime_pe_ep.code].mktcap/10000, 2) if codes_map[realtime_pe_ep.code].mktcap else 0
            if code in buffetts_map:
                realtime_pe_ep.flow_sub_total = buffetts_map[realtime_pe_ep.code].flow_sub_total
                realtime_pe_ep.flow_sub_flow = buffetts_map[realtime_pe_ep.code].flow_sub_flow
                realtime_pe_ep.pb = buffetts_map[realtime_pe_ep.code].pb
            #if not (realtime_pe_ep.industry == '普钢' or realtime_pe_ep.industry == '银行' or realtime_pe_ep.industry == '特种钢'):
            ret.append(realtime_pe_ep)
        logging.info("ret cnt: %s", len(ret))
        return ret
    except Exception as e:
        traceback.print_exc()
    finally:
        session.close()


def get_total_wroe_ranking_row():
    try:
        latest_record_date = get_latest_record_date()
        cnt = session.query(func.count(Zycwzb.id)).filter(and_(Zycwzb.date == latest_record_date)).scalar()
        return cnt
    except Exception as e:
        traceback.print_exc()
    finally:
        session.close()


def get_wroe_ranking_datas(page, pageSize, paramcodes=None, market_time_in=None):
    try:
        """
            获取根据roe排名的股票数据
        :return:
        """
        page = 0 if not page else page
        pageSize = 100 if not pageSize else pageSize
        offset = page * pageSize
        latest_year_report = latest_record_date = get_latest_record_date()
        if not latest_record_date.endswith("12-31"):
            latest_year_report = get_pre_yearreport_date(latest_record_date)
        logging.info("latest_year_report: %s", latest_year_report)
        # 获取wroe排名前100的数据
        zycwzbs = session.query(Zycwzb).filter(and_(Zycwzb.date == latest_year_report, Zycwzb.code.in_(paramcodes) if len(paramcodes) > 0 else 1==1)).order_by(desc(Zycwzb.kfroe)).limit(pageSize).offset(offset).all()
        logging.info("获取主要财务指标数据OK")
        codes = get_codes(zycwzbs)

        zcfzbs = getSession().query(Zcfzb).filter(and_(Zcfzb.date == latest_year_report, Zcfzb.code.in_(codes))).all()
        logging.info("获取资产负债表数据OK.")
        zcfzbs_map = {}
        for zcfzbi in zcfzbs:
            zcfzbs_map[zcfzbi.code] = zcfzbi

        hist_max_date_record = session.query(func.max(HistData.date)).filter(HistData.code.in_(codes)).first()
        hist_max_date = hist_max_date_record[0]
        logging.info("获取价格的日期为: %s", hist_max_date)

        hist_datas = session.query(HistData).filter(and_(HistData.date == hist_max_date, HistData.code.in_(codes))).all()
        logging.info("获取价格数据ok.")
        hist_datas_map = {}
        for hist_datas_i in hist_datas:
            hist_datas_map[hist_datas_i.code] = hist_datas_i

        stocks = session.query(StockInfo).filter(StockInfo.code.in_(codes)).all()
        stocks_map = get_stocks_map(stocks)

        realtimepeepss = session.query(RealTimePEEPS).filter(RealTimePEEPS.code.in_(codes)).all()
        realtimepeeps_map = build_map(realtimepeepss)

        ret = []
        filter_date_start = None
        if market_time_in is not None:
            filter_date_start = (datetime.date.today() - datetime.timedelta(days=int(market_time_in) * 365)).strftime('%Y%m%d')
        for zycwzb in zycwzbs:
            code = zycwzb.code
            name = zycwzb.name
            stock_info = stocks_map[code]
            if market_time_in is not None and filter_date_start is not None and stock_info.timeToMarket <= filter_date_start:
                logging.info("%s %s 上市时间 %s 非 %s 年以内", code, name, market_time_in, stock_info.timeToMarket)
                continue
            if stock_info.mktcap is None:
                logging.info("%s %s 无市值数据，是新股？", code, name)
                continue

            zcfzb = zcfzbs_map[code]
            # 负债率
            liab_ratio = zcfzb.liab_ratio if zcfzb is not None else None
            non_current_liab_ratio = zcfzb.non_current_liab_ratio if zcfzb is not None else None
            zycwzb.liab_ratio = liab_ratio
            zycwzb.non_current_liab_ratio = non_current_liab_ratio
            zycwzb.net_assets = round((zycwzb.total_assets - zycwzb.total_debts)/10000, 2)
            zycwzb.industry = stock_info.industry
            zycwzb.variance = round(abs(zycwzb.net_profit - zycwzb.npad) / zycwzb.net_profit, 2) if zycwzb.net_profit != 0 else 0
            zycwzb.mktcap = round(stock_info.mktcap / 10000, 2)
            if code in hist_datas_map:
                zycwzb.price = hist_datas_map[code].close
            else:
                logging.warning("%s 没有最新价格.", code)
            if code in realtimepeeps_map:
                if not hasattr(zycwzb, 'price'):
                    logging.info("%s 使用realtimepeeps的最新价格(可能不实时)", code)
                    zycwzb.price = realtimepeeps_map[code].price
                zycwzb.eps = realtimepeeps_map[code].eps1
                zycwzb.pe = realtimepeeps_map[code].pe1
                zycwzb.lastyear_pe = realtimepeeps_map[code].pe2
                zycwzb.koufei_pe = realtimepeeps_map[code].koufei_pe
                zycwzb.predict_pe = realtimepeeps_map[code].predict_pe if realtimepeeps_map[code].predict_pe else 0
                zycwzb.predict_price = round(zycwzb.eps * zycwzb.predict_pe, 2)
                if liab_ratio < 60 and non_current_liab_ratio < 30:
                    #logging.info("%s %s PE: %s, 扣非PE: %s, 负债率: %s, 非流动负债率: %s", code, name, zycwzb.pe, zycwzb.koufei_pe, liab_ratio, non_current_liab_ratio)
                    zycwzb.good = 1
                if liab_ratio < 60 and non_current_liab_ratio < 10:
                    logging.info("%s %s %s PE: %s, 扣非PE: %s, 负债率: %s, 非流动负债率: %s", code, name, zycwzb.industry, zycwzb.pe, zycwzb.koufei_pe, liab_ratio, non_current_liab_ratio)
                    zycwzb.verygood = 1
            else:
                logging.warning("%s realtimepeeps最新信息没找到.", code)
            ret.append(zycwzb)
        logging.info(": %s", len(ret))

        return ret
    except Exception as e:
        traceback.print_exc()
    finally:
        session.close()


def get_netflow_ranking_datas(page, pageSize):
    try:
        """
            获取根据pe排名的股票数据
        :return:
        """
        page = 0 if not page else page
        pageSize = 100 if not pageSize else pageSize
        offset = page * pageSize
        latest_record_date = get_latest_record_date()
        # 获取wroe排名前100的数据
        buffets = session.query(Buffett).order_by(Buffett.flow_sub_total).limit(pageSize).offset(offset).all()
        codes = get_codes(buffets)

        stocks = session.query(StockInfo).filter(StockInfo.code.in_(codes)).all()
        stocks_map = get_stocks_map(stocks)

        realtimepeepss = session.query(RealTimePEEPS).filter(RealTimePEEPS.code.in_(codes)).all()
        realtimepeeps_map = build_map(realtimepeepss)

        zycwzbs = session.query(Zycwzb).filter(Zycwzb.code.in_(codes)).all()
        zycwzbs_map = build_map(zycwzbs)

        ret = []
        for buffet in buffets:
            code = buffet.code
            name = buffet.name
            logging.info("%s %s", code, name)
            buffet.industry = stocks_map[code].industry
            buffet.mktcap = round(stocks_map[code].mktcap / 10000, 2)
            buffet.price = realtimepeeps_map[code].price
            buffet.pe = realtimepeeps_map[code].pe1
            buffet.koufei_pe = realtimepeeps_map[code].koufei_pe
            buffet.eps = realtimepeeps_map[code].eps1
            buffet.wroe = zycwzbs_map[code].wroe

            ret.append(buffet)
        logging.info("return cnt: %s", len(ret))

        return ret
    except Exception as e:
        traceback.print_exc()
    finally:
        session.close()


def get_pb_ranking_datas(page, pageSize, sort_by):
    try:
        """
            获取根据pe排名的股票数据
        :return:
        """
        page = 0 if not page else int(page)
        pageSize = 100 if not pageSize else int(pageSize)
        offset = page * pageSize
        #latest_record_date = get_latest_record_date()
        # 获取wroe排名前100的数据
        sort_by_field = RealTimePB.pb
        if sort_by == 'liab_ratio':
            sort_by_field = RealTimePB.liab_ratio
        if sort_by == 'non_current_liab_ratio':
            sort_by_field = RealTimePB.non_current_liab_ratio
        rankingpbs = session.query(RealTimePB).filter(and_(RealTimePB.pb.isnot(None))).order_by(sort_by_field).limit(pageSize).offset(offset).all()
        codes = get_codes(rankingpbs)

        stocks = session.query(StockInfo).filter(StockInfo.code.in_(codes)).all()
        stocks_map = get_stocks_map(stocks)

        #realtimepeepss = session.query(RealTimePEEPS).filter(RealTimePEEPS.code.in_(codes)).all()
        #realtimepeeps_map = build_map(realtimepeepss)

        zycwzbs = session.query(Zycwzb).filter(Zycwzb.code.in_(codes)).all()
        zycwzbs_map = build_map(zycwzbs)

        ret = []
        for rankingpb in rankingpbs:
            code = rankingpb.code
            name = rankingpb.name
            logging.info("%s %s", code, name)
            if code not in stocks_map:
                continue
            rankingpb.industry = stocks_map[code].industry
            rankingpb.mktcap = round(stocks_map[code].mktcap / 10000, 2)

            ret.append(rankingpb)
        logging.info("return cnt: %s", len(ret))

        return ret
    except Exception as e:
        traceback.print_exc()
    finally:
        session.close()


def get_reports_detail(code, start_date, end_date):
    try:
        start_date = start_date if start_date else '2006-12-31'
        end_date = end_date if end_date else get_latest_record_date()
        zycwzbs = session.query(Zycwzb).filter(and_(Zycwzb.code == code,
                                                           Zycwzb.date >= start_date,
                                                           Zycwzb.date <= end_date)).order_by(desc(Zycwzb.date)).all()
        return zycwzbs
    except Exception as e:
        traceback.print_exc()
    finally:
        session.close()


def get_hist_prices_map(matched_codes):
    try:
        ## 查出股票一年内、两年内涨幅、三年内、五年内涨幅
        today = datetime.date.today()
        today_str = today.strftime('%Y-%m-%d %H:%M:%S')
        year_before = (today - datetime.timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
        two_years_before = (today - datetime.timedelta(days=365 * 2)).strftime('%Y-%m-%d %H:%M:%S')
        three_years_before = (today - datetime.timedelta(days=365 * 3)).strftime('%Y-%m-%d %H:%M:%S')
        four_years_before = (today - datetime.timedelta(days=365 * 4)).strftime('%Y-%m-%d %H:%M:%S')
        five_years_before = (today - datetime.timedelta(days=365 * 5)).strftime('%Y-%m-%d %H:%M:%S')

        sub_q_max = aliased(session.query(HistData.code, func.max(HistData.date).label('max_date')).filter(
            and_(HistData.date >= year_before, HistData.code.in_(matched_codes))).group_by(HistData.code).subquery())
        max_hist = session.query(sub_q_max, HistData.close).join(HistData, and_(HistData.code == sub_q_max.c.code,
                                                                                    HistData.date == sub_q_max.c.max_date)).all()
        max_hist_map = {}
        for max_hist_i in max_hist:
            max_hist_map[max_hist_i.code] = max_hist_i

        #以下sql语句的翻译：select h.code,h.name,h.date,h.close from (select code,min(date) min_date from hist_data where code in ('000895','000651','600519', '000333', '000002') and date >= '2016-07-04' group by code) t join hist_data h on t.code = h.code and h.date = t.min_date
        # 获取前1年的价格
        sub_q = aliased(session.query(HistData.code, func.min(HistData.date).label('min_date')).filter(and_(HistData.date >= year_before, HistData.code.in_(matched_codes))).group_by(HistData.code).subquery())
        year_before_hist = session.query(sub_q, HistData.close).join(HistData, and_(HistData.code == sub_q.c.code, HistData.date == sub_q.c.min_date)).all()
        year_before_map = {}
        for year_before_i in year_before_hist:
            year_before_map[year_before_i.code] = year_before_i
        ret_map = {}
        for code_i in matched_codes:
            if code_i not in ret_map:
                ret_map[code_i] = []
                ret_map[code_i].append(max_hist_map[code_i] if code_i in max_hist_map else {})
            ret_map[code_i].append(year_before_map[code_i] if code_i in year_before_map else {})

        # 获取前2年的价格
        sub_q = aliased(session.query(HistData.code, func.min(HistData.date).label('min_date')).filter(and_(HistData.date >= two_years_before, HistData.code.in_(matched_codes))).group_by(HistData.code).subquery())
        two_year_before_hist = session.query(sub_q, HistData.close).join(HistData, and_(HistData.code == sub_q.c.code, HistData.date == sub_q.c.min_date)).all()
        two_year_before_map = {}
        for two_year_before_i in two_year_before_hist:
            two_year_before_map[two_year_before_i.code] = two_year_before_i

        for code_i in matched_codes:
            if code_i not in ret_map:
                ret_map[code_i] = []
                ret_map[code_i].append(max_hist_map[code_i] if code_i in max_hist_map else {})
            ret_map[code_i].append(two_year_before_map[code_i] if code_i in two_year_before_map else {})

        # 获取前3年的价格
        sub_q = aliased(session.query(HistData.code, func.min(HistData.date).label('min_date')).filter(and_(HistData.date >= three_years_before, HistData.code.in_(matched_codes))).group_by(HistData.code).subquery())
        three_year_before_hist = session.query(sub_q, HistData.close).join(HistData, and_(HistData.code == sub_q.c.code, HistData.date == sub_q.c.min_date)).all()
        three_year_before_map = {}
        for three_year_before_i in three_year_before_hist:
            three_year_before_map[three_year_before_i.code] = three_year_before_i

        for code_i in matched_codes:
            if code_i not in ret_map:
                ret_map[code_i] = []
                ret_map[code_i].append(max_hist_map[code_i] if code_i in max_hist_map else {})
            ret_map[code_i].append(three_year_before_map[code_i] if code_i in three_year_before_map else {})

        # 获取前4年的价格
        sub_q = aliased(session.query(HistData.code, func.min(HistData.date).label('min_date')).filter(and_(HistData.date >= four_years_before, HistData.code.in_(matched_codes))).group_by(HistData.code).subquery())
        four_year_before_hist = session.query(sub_q, HistData.close).join(HistData, and_(HistData.code == sub_q.c.code, HistData.date == sub_q.c.min_date)).all()
        four_year_before_map = {}
        for four_year_before_i in four_year_before_hist:
            four_year_before_map[four_year_before_i.code] = four_year_before_i

        for code_i in matched_codes:
            if code_i not in ret_map:
                ret_map[code_i] = []
                ret_map[code_i].append(max_hist_map[code_i] if code_i in max_hist_map else {})
            ret_map[code_i].append(four_year_before_map[code_i] if code_i in four_year_before_map else {})

        # 获取前5年的价格
        sub_q = aliased(session.query(HistData.code, func.min(HistData.date).label('min_date')).filter(and_(HistData.date >= five_years_before, HistData.code.in_(matched_codes))).group_by(HistData.code).subquery())
        five_year_before_hist = session.query(sub_q, HistData.close).join(HistData, and_(HistData.code == sub_q.c.code, HistData.date == sub_q.c.min_date)).all()
        five_year_before_map = {}
        for five_year_before_i in five_year_before_hist:
            five_year_before_map[five_year_before_i.code] = five_year_before_i

        for code_i in matched_codes:
            if code_i not in ret_map:
                ret_map[code_i] = []
                ret_map[code_i].append(max_hist_map[code_i] if code_i in max_hist_map else {})
            ret_map[code_i].append(five_year_before_map[code_i] if code_i in five_year_before_map else {})


        """
        # 最近的价格日期, 000002是万科的代码，这里只是方便筛选数据使用
        now_date_str = session.query(func.max(HistData.date)).filter(HistData.code == '000002').first()[0]
        year_before_str = session.query(func.min(HistData.date)).filter(HistData.code == '000002', HistData.date >= year_before).first()[
            0]
        two_years_before_str = session.query(func.min(HistData.date)).filter(HistData.code == '000002',
                                                                             HistData.date >= two_years_before).first()[
            0]
        three_years_before_str = session.query(func.min(HistData.date)).filter(HistData.code == '000002',
                                                                               HistData.date >= three_years_before).first()[
            0]
        four_years_before_str = session.query(func.min(HistData.date)).filter(HistData.code == '000002',
                                                                              HistData.date >= four_years_before).first()[
            0]
        five_years_before_str = session.query(func.min(HistData.date)).filter(HistData.code == '000002',
                                                                              HistData.date >= five_years_before).first()[
            0]
        search_hist_dates = [now_date_str, year_before_str, two_years_before_str, three_years_before_str,
                             four_years_before_str, five_years_before_str]

        logging.info("search_hist_dates: %s", search_hist_dates)
        hist_datas = session.query(HistData).filter(and_(HistData.code.in_(matched_codes),
                                                         HistData.date.in_(search_hist_dates))).order_by(
            desc(HistData.date)).all()
        hist_datas_map = {}
        for hist_data_i in hist_datas:
            code_i = hist_data_i.code
            if code_i not in hist_datas_map:
                hist_datas_map[code_i] = []
            hist_datas_map[code_i].append(hist_data_i)"""
        return ret_map
    except Exception as e:
        traceback.print_exc()
    finally:
        session.close()


def get_incre(hist_price_arr, years):
    try:
        if len(hist_price_arr) < 1:
            return None
        if years == 1:
            if len(hist_price_arr) < 2:
                return None
            return round((hist_price_arr[0].close - hist_price_arr[1].close) * 100 / hist_price_arr[1].close, 2)
        if years == 2:
            if len(hist_price_arr) < 3:
                return None
            return round((hist_price_arr[0].close - hist_price_arr[2].close) * 100 / hist_price_arr[2].close, 2)
        if years == 3:
            if len(hist_price_arr) < 4:
                return None
            return round((hist_price_arr[0].close - hist_price_arr[3].close) * 100 / hist_price_arr[3].close, 2)
        if years == 4:
            if len(hist_price_arr) < 5:
                return None
            return round((hist_price_arr[0].close - hist_price_arr[4].close) * 100 / hist_price_arr[4].close, 2)
        if years == 5:
            if len(hist_price_arr) < 6:
                return None
            return round((hist_price_arr[0].close - hist_price_arr[5].close) * 100 / hist_price_arr[5].close, 2)
    except Exception as e:
        traceback.print_exc()
    finally:
        session.close()


def get_continuous_high_roe_codes(continuous_years, roe):
    try:
        # 最近一年
        latest_year_report = get_pre_yearreport_date(get_latest_record_date())
        # latest_year_report = get_pre_yearreport_date(get_pre_yearreport_date(get_pre_yearreport_date(get_pre_yearreport_date(latest_year_report))))
        logging.info("latest_year_report: %s", latest_year_report)
        search_years = [latest_year_report]
        one_year_before = latest_year_report
        for i in range(1, continuous_years):
            one_year_before = get_pre_yearreport_date(one_year_before)
            search_years.append(one_year_before)
        logging.info('查询年份: %s', search_years)
        matched_records = session.query(Zycwzb.code, func.count(Zycwzb.code)).\
            filter(and_(Zycwzb.kfroe >= roe, Zycwzb.date.in_(search_years))).\
            group_by(Zycwzb.code).having(func.count(Zycwzb.code) >= continuous_years).all()
        logging.info('cnt: %s, searched_codes : %s', len(matched_records), matched_records)
        matched_codes = []
        for record_i in matched_records:
            matched_codes.append(record_i[0])
        zycwzbs = session.query(Zycwzb).filter(and_(Zycwzb.code.in_(matched_codes), Zycwzb.date == latest_year_report)).\
            order_by(desc(Zycwzb.kfroe)).all()
        stocks = session.query(StockInfo).filter(StockInfo.code.in_(matched_codes)).all()
        stocks_map = get_stocks_map(stocks)
        # 获取1年前。。至5年前的价格
        hist_map = get_hist_prices_map(matched_codes)
        ret = []
        for zycwzb_i in zycwzbs:
            code = zycwzb_i.code
            name = zycwzb_i.name
            if code not in stocks_map:
                continue
            stock_info = stocks_map[code]
            zycwzb_i.industry = stock_info.industry
            zycwzb_i.industry_classified = stock_info.industry_classified
            zycwzb_i.pe = stock_info.pe
            zycwzb_i.mktcap = round(stock_info.mktcap / 10000, 2)
            zycwzb_i.timeToMarket = stock_info.timeToMarket
            # 上市时间晚于查询的时间最后一个年份
            zycwzb_i.timeIsFull = False if stock_info.timeToMarket > search_years[-1] else True
            timeToMarketYear = int(stock_info.timeToMarket[0:4])
            logging.info("code: %s, len_price_hist: %s", zycwzb_i.code, len(hist_map[zycwzb_i.code]))
            zycwzb_i.year_incre = get_incre(hist_map[zycwzb_i.code], 1)
            zycwzb_i.two_year_incre = get_incre(hist_map[zycwzb_i.code], 2)
            zycwzb_i.three_year_incre = get_incre(hist_map[zycwzb_i.code], 3)
            zycwzb_i.four_year_incre = get_incre(hist_map[zycwzb_i.code], 4)
            zycwzb_i.five_year_incre = get_incre(hist_map[zycwzb_i.code], 5)
            if (int(latest_year_report[0:4]) - timeToMarketYear) <= continuous_years:
                logging.info("%s %s 上市时间 %s，忽略", code, name, timeToMarketYear)
                zycwzb_i.newStock = True
            else:
                ret.append(zycwzb_i)

        return ret
    except Exception as e:
        traceback.print_exc()
    finally:
        session.close()


if __name__ == '__main__':
    pass
