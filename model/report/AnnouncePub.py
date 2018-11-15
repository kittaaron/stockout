__author__ = 'kittaaron'

from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AnnouncePub(Base):
    __tablename__ = 'announce_pub'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票代码
    name = Column(String)
    # 年份
    title = Column(String)
    # 年份
    pub_date = Column(String)
    # 年份
    file_url = Column(String)
    # 年份
    bulletin_type = Column(String)
    # 年份
    bulletin_year = Column(String)

    def __str__(self):
        msg = "code:" + self.code + ",name: " + self.name
        return msg
