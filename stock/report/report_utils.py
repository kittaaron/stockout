import datetime


def get_latest_record_date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    if 1 <= month <= 4:
        year -= 1
        return str(year) + "-" + "12-31"
    elif 5 <= month <= 8:
        return str(year) + "-" + "03-31"
    elif 9 <= month <= 10:
        return str(year) + "-" + "06-30"
    elif 11 <= month:
        return str(year) + "-" + "09-30"
    else:
        return None


def get_pre_yearreport_date(date_str):
    year = int(date_str[0:4]) - 1
    return str(year) + "-" + "12-31"


def get_multiple(date):
    """
        根据报表日期，返回一个乘数。比如1季度的报表，利润等都要乘以4
    :param date:
    :return:
    """
    month = datetime.datetime.now().month

    date_no_year = date[(len(date) - 5):]
    if date_no_year == '03-31':
        return 4
    if date_no_year == '06-30':
        return 2
    if date_no_year == '09-30':
        return 4 / 3
    if date_no_year == '12-31':
        return 1