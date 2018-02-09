
from datetime import datetime, date
from decimal import Decimal
import json


class serializable_them(json.JSONEncoder):
    """
    有些类型是不能序列化的. 我现在要让他们能序列化.

    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, Decimal):
            return str(obj)

        return json.JSONEncoder.default(self, obj)


def rotate_letter(letter, n):
    """
    ROT13基础算法
    :param letter:
    :param n:
    :return:
    """
    if letter.isupper():
        start = ord('A')
    elif letter.islower():
        start = ord('a')
    else:
        return letter


    c = ord(letter) - start
    i = (c + n) % 26 + start
    return chr(i)




def rotate_word(word, n):
    """
    使用ROT13来验证重置密码时候的vcode,避免mid外漏带来高危漏洞
    :param word:
    :param n:
    :return:
    """
    res = ''
    for letter in word:
        res += rotate_letter(letter, n)
    return res