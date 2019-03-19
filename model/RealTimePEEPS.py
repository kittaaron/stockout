__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RealTimePEEPS(Base):
    __tablename__ = 'realtime_pe_eps'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    koufei_pe = Column(DECIMAL)
    pe1 = Column(DECIMAL)
    pe2 = Column(DECIMAL)
    pe3 = Column(DECIMAL)
    pe4 = Column(DECIMAL)
    koufei_eps = Column(DECIMAL)
    eps1 = Column(DECIMAL)
    eps2 = Column(DECIMAL)
    eps3 = Column(DECIMAL)
    eps4 = Column(DECIMAL)
    price = Column(DECIMAL)
    predict_pe = Column(Integer)
    eval_price = Column(DECIMAL)
    eval_price_ratio = Column(DECIMAL)
    std_devi = Column(DECIMAL)
    liab_ratio = Column(DECIMAL)
    non_current_liab_ratio = Column(DECIMAL)

    latest_report_date = Column(String)
    date = Column(String)

    def __int__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        msg = self.code + " " + self.name
        return msg

    def reprJSON(self):
        ret = {}
        for item in self.__dict__.items():
            key = item[0]
            val = item[1]
            if key.startswith("_"):
                continue
            ret[key] = val
        return ret
        """
        return dict(code=self.code, name=self.name, koufei_pe=self.koufei_pe, pe1=self.pe1,
                    pe2=self.pe2, pe3=self.pe3, pe4=self.pe4,
                    koufei_eps=self.koufei_eps, eps1=self.eps1,
                    eps2=self.eps2, eps3=self.eps3, eps4=self.eps4, price=self.price,
                    eval_price=self.eval_price, eval_price_ratio=self.eval_price_ratio, std_devi=self.std_devi,
                    latest_report_date=self.latest_report_date, date=self.date)
        """
