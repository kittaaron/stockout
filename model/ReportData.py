__author__ = 'kittaaron'

from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ReportData(Base):
    __tablename__ = 'report_data'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票代码
    name = Column(String)
    # 年份
    year = Column(Integer)
    # 季度
    season = Column(Integer)
    # 每股收益
    eps = Column(DECIMAL)
    # 每股收益同比(%)
    eps_yoy = Column(DECIMAL)
    # 每股净资产
    bvps = Column(DECIMAL)
    # 净资产收益率(%)
    roe = Column(DECIMAL)
    # 每股现金流量(元)
    epcf = Column(DECIMAL)
    # 净利润(万元)
    net_profits = Column(DECIMAL)
    # 净利润同比(%)
    profits_yoy = Column(DECIMAL)
    # 分配方案
    distrib = Column(String)
    # 报告日期
    report_date = Column(DECIMAL)
    # 净利率(%)
    net_profit_ratio = Column(DECIMAL)
    # 毛利率(%)
    gross_profit_rate = Column(DECIMAL)
    # 营业收入(百万元)
    business_income = Column(DECIMAL)
    # 每股主营业务收入(元)
    bips = Column(DECIMAL)
    # 应收账款周转率(次)
    arturnover = Column(DECIMAL)
    # 应收账款周转天数(天)
    arturndays = Column(DECIMAL)
    # 存货周转率(次)
    inventory_turnover = Column(DECIMAL)
    # 存货周转天数(天)
    inventory_days = Column(DECIMAL)
    # 流动资产周转率(次)
    currentasset_turnover = Column(DECIMAL)
    # 流动资产周转天数(天)
    currentasset_days = Column(DECIMAL)
    # 主营业务收入增长率(%)
    mbrg = Column(DECIMAL)
    # 净利润增长率(%)
    nprg = Column(DECIMAL)
    # 净资产增长率
    nav = Column(DECIMAL)
    # 总资产增长率
    targ = Column(DECIMAL)
    # 每股收益增长率
    epsg = Column(DECIMAL)
    # 股东权益增长率
    seg = Column(DECIMAL)
    # 流动比率
    currentratio = Column(DECIMAL)
    # 速动比率
    quickratio = Column(DECIMAL)
    # 现金比率
    cashratio = Column(DECIMAL)
    # 利息支付倍数
    icratio = Column(DECIMAL)
    # 股东权益比率
    sheqratio = Column(DECIMAL)
    # 股东权益增长率
    adratio = Column(DECIMAL)
    # 经营现金净流量对销售收入比率
    cf_sales = Column(DECIMAL)
    # 资产的经营现金流量回报率
    rateofreturn = Column(DECIMAL)
    # 经营现金净流量与净利润的比率
    cf_nm = Column(DECIMAL)
    # 经营现金净流量对负债比率
    cf_liabilities = Column(DECIMAL)
    # 现金流量比率
    cashflowratio = Column(DECIMAL)

    def __str__(self):
        msg = "code:" + self.code + ",name: " + self.name + ",year season: " + str(self.year) + "," + str(self.season) + ",esp: " + str(self.eps)\
             + ",eps_yoy: " + str(self.eps_yoy)+ ",roe: " + str(self.roe)+ ",profits_yoy: " + str(self.profits_yoy)\
            + ",distrib: " + str(self.distrib)
        return msg