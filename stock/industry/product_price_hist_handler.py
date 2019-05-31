__author__ = 'kittaaron'

from sqlalchemy import and_
from utils.db_utils import *
from model.ProductHistPrice import ProductHistPrice
from model.ProductTypeConf import ProductTypeConf
import config.logginconfig
import logging


session = getSession()


def get_grouped_category1(category0, dateform, dateto):
    ret = {}
    records = get_category0_price_list(category0, dateform, dateto)
    if records is None:
        return ret
    for record_i in records:
        categoryi1 = record_i.category1
        if categoryi1 not in ret:
            ret[categoryi1] = []
        ret[categoryi1].append(record_i)
    return ret


def get_category0_price_list(category0, dateform, dateto):
    try:
        records = session.query(ProductHistPrice).filter(and_(ProductHistPrice.category0 == category0,
                                                              ProductHistPrice.date >= dateform,
                                                              ProductHistPrice.date <= dateto,
                                                              )).order_by(ProductHistPrice.category1, ProductHistPrice.date).all()
        return records
    except Exception as e:
        pass
    finally:
        session.close()


def get_category1_price_list(category0, category1, dateform, dateto):
    try:
        records = session.query(ProductHistPrice).filter(and_(ProductHistPrice.category0 == category0,
                                                              ProductHistPrice.category1 == category1,
                                                              ProductHistPrice.date >= dateform,
                                                              ProductHistPrice.date <= dateto,
                                                              )).all()
        return records
    except Exception as e:
        pass
    finally:
        session.close()


def get_category0_def_list():
    try:
        records = session.query(ProductTypeConf).filter(and_(ProductTypeConf.parent_id == 0)).all()
        return records
    except Exception as e:
        pass
    finally:
        session.close()


def get_category1_def_list(category0_id):
    try:
        records = session.query(ProductTypeConf).filter(and_(ProductTypeConf.parent_id == category0_id)).all()
        return records
    except Exception as e:
        pass
    finally:
        session.close()


def save_product_price(c0, c1, date, price):
    try:
        old_obj = session.query(ProductHistPrice).filter(and_(ProductHistPrice.category0 == c0,
                                                    ProductHistPrice.category1 == c1,
                                                    ProductHistPrice.date == date,
                                                    )).first()
        if old_obj is None:
            old_obj = ProductHistPrice(category0=c0, category1=c1, date=date, price=price)
        else:
            old_obj.price = price
        session.add(old_obj)
        session.commit()
        logging.info("保存价格成功")
        return
    except Exception as e:
        logging.error(e)
        pass
    finally:
        session.close()


def batch_save_product_price(c0, date, names, prices):
    # 调用单个插入的函数
    for idx, name in enumerate(names):
        logging.info("c0: %s, c1: %s, date: %s, price: %s", c0, name, date, prices[idx])
        save_product_price(c0, name, date, prices[idx])


if __name__ == '__main__':
    pass
