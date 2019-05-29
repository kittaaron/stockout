__author__ = 'kittaaron'

from sqlalchemy import and_
from utils.db_utils import *
from model.ProductHistPrice import ProductHistPrice


session = getSession()


def get_grouped_category1(category0, dateform, dateto):
    ret = {}
    records = get_category0_list(category0, dateform, dateto)
    for record_i in records:
        categoryi1 = record_i.category1
        if categoryi1 not in ret:
            ret[categoryi1] = []
        ret[categoryi1].append(record_i)
    return ret


def get_category0_list(category0, dateform, dateto):
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


def get_category1_list(category0, category1, dateform, dateto):
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


if __name__ == '__main__':
    pass
