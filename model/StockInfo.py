__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class StockInfo(Base):
    __tablename__ = 'stockinfo'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    # 股票汉字拼音首字母(小写)
    abbr = Column(String)
    # 股票行业
    industry = Column(String)
    # 行业分类
    industry_classified = Column(String)
    # 概念分类
    concept_classified = Column(String)
    # 股票地区
    area = Column(String)
    # 市盈率(市价P/盈利Earning比率)
    pe = Column(DECIMAL)
    # 市净率(市价P/Book value净资产)
    pb = Column(DECIMAL)
    # 流通股本(亿)
    outstanding = Column(BigInteger)
    # 总股本(亿)
    totals = Column(DECIMAL)
    # 总资产(万)
    totalAssets = Column(DECIMAL)
    # 流动资产
    liquidAssets = Column(DECIMAL)
    # 固定资产
    fixedAssets = Column(DECIMAL)
    # 资本公积???
    reserved = Column(DECIMAL)
    # 每股
    reservedPerShare = Column(DECIMAL)
    # 每股收益(Earnings Per Share)
    esp = Column(DECIMAL)
    # bvps 每股净资产
    bvps = Column(DECIMAL)
    # 上市时间
    timeToMarket = Column(String)
    # 未分配利润
    undp = Column(DECIMAL)
    # 每股未分配
    perundp = Column(DECIMAL)
    # 收入同比(%)
    rev = Column(DECIMAL)
    # profit,利润同比(%)
    profit = Column(DECIMAL)
    # gpr,毛利率(%)
    gpr = Column(DECIMAL)
    # 净利润率(%)
    npr = Column(DECIMAL)
    #
    mktcap = Column(DECIMAL)
    #
    holders = Column(Integer)
    issz50 = Column(Integer)
    iszz500 = Column(Integer)

    def __str__(self):
        msg = "code:" + self.code + ",name: " + self.name + ",pe: " + str(self.pe);
        return msg

    class StockInfoEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__

    def reprJSON(self):
        return dict(code=self.code, name=self.name, industry=self.industry, industry_classified=self.industry_classified,
                    pe=self.pe, totals=self.totals, area=self.area,
                    bvps=self.bvps, concept_classified=self.concept_classified, esp=self.esp, fixedAssets=self.fixedAssets,
                    gpr=self.gpr, holders=self.holders,
                    liquidAssets=self.liquidAssets, mktcap=self.mktcap, npr=self.npr, outstanding=self.outstanding,
                    pb=self.pb, perundp=self.perundp, profit=self.profit,
                    reserved=self.reserved, reservedPerShare=self.reservedPerShare, rev=self.rev,
                    timeToMarket=self.timeToMarket, totalAssets=self.totalAssets, undp=self.undp)