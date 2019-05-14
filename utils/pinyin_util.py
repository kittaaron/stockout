# -*- coding: utf-8 -*-

from pypinyin import pinyin, lazy_pinyin, Style


def get_acronym(str_data):
    """
    获取字符串的首字母
    :param str_data: 字符串
    :return: 字符串
    """
    return "".join([i[0][0] for i in pinyin(str_data, style=Style.FIRST_LETTER)])