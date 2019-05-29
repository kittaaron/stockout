__author__ = 'kittaaron'

"""
    用csv文件导入维生素历史价格
"""

import config.logginconfig
import logging
import csv
from utils.db_utils import *
from model.ProductHistPrice import ProductHistPrice
import dateutil.parser


session = getSession()


def import_vit_price(file_path):
    csv_file = csv.reader(open(file_path, 'r'))
    headers = []
    # 标记是否是头部(第一行)
    idx = 0
    for line in csv_file:
        if idx == 0:
            headers = line[1:]
            idx += 1
            continue
        category0 = "维生素"
        date = dateutil.parser.parse(line[0]).strftime("%Y-%m-%d")
        logging.info("date: %s", date)
        price_list = []
        for i, val in enumerate(line):
            if i == 0:
                continue
            category1 = headers[i-1]
            price = round(float(val), 2)
            obj = ProductHistPrice(category0 = category0, category1 = category1, date = date, price = price)
            price_list.append(obj)

        session.add_all(price_list)
        session.commit()
        logging.info("add ok.")


if __name__ == '__main__':
    import_vit_price('/Users/kittaaron/Downloads/2018年维生素价格跟踪2019-05-28.csv')