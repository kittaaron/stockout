__author__ = 'kittaaron'

import config.logginconfig
import model.StockInfo
from stock import basic
import logging

if __name__ == '__main__':
    logging.info("bootstrap run.")
    basic.update_stock_basics()
