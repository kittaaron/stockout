import datetime
from model.Holiday import Holiday
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig
from utils.db_utils import *

session = getSession()


def get_next_transact_date(date_str):
    now_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    next_date = now_date + datetime.timedelta(days=1)
    is_transact_date = False
    while is_transact_date is False:
        next_date_str = next_date.strftime('%Y-%m-%d')
        holiday_date = session.query(Holiday).filter(Holiday.holiday_date == next_date_str).first()
        if holiday_date is None:
            is_transact_date = True
        else:
            next_date += datetime.timedelta(days=1)

    return next_date.strftime('%Y-%m-%d')


def get_pre_transact_date(date_str):
    now_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    next_date = now_date - datetime.timedelta(days=1)
    is_transact_date = False
    while is_transact_date is False:
        next_date_str = next_date.strftime('%Y-%m-%d')
        holiday_date = session.query(Holiday).filter(Holiday.holiday_date == next_date_str).first()
        if holiday_date is None:
            is_transact_date = True
        else:
            next_date -= datetime.timedelta(days=1)

    return next_date.strftime('%Y-%m-%d')


def is_holiday(date_str):
    holiday_date = session.query(Holiday).filter(Holiday.holiday_date == date_str).first()
    return holiday_date is not None