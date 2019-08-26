# -*- coding: utf-8 -*-
# @Author kittaaron

from twilio.rest import Client
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

account_sid = "AC4fdaa08e24fc9c5d7462558a03031a20"
auth_token = "twilio32位长token"

client = Client(account_sid, auth_token)


def sendMsg(msg):
    message = client.messages.create(
        #to="+8615622813257",
        to="+8615622813257",
        from_="+18125583488",
        body=msg
)


def sendMsgTX(params, template_id):
    sms_type = 0  # Enum{0: 普通短信, 1: 营销短信}
    phone_numbers = ['15622813257']
    ssender = SmsSingleSender('1400150141', 'ec094fa8790625ba7ad182d8c634f184')
    #params = ['茅台', '14']
    try:
        result = ssender.send_with_param(86, phone_numbers[0],
                                         template_id, params, sign='', extend="",
                                         ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)


def sendAttentionMsgTX(params):
    template_id = 301736
    sendMsgTX(params, template_id)


def sendRecommendMsgTX(params):
    template_id = 302764
    sendMsgTX(params, template_id)


def sendIntrinsicDiscountMsgTX(params):
    template_id = 398484
    sendMsgTX(params, template_id)


if __name__ == '__main__':
    sendMsgTX("测试腾讯云短信")