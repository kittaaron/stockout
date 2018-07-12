# -*- coding: utf-8 -*-
# @Author kittaaron

from twilio.rest import Client

account_sid = "AC4fdaa08e24fc9c5d7462558a03031a20"
auth_token = "e49e6f3df3826e5d0a85d856520bf9f7"

client = Client(account_sid, auth_token)

def sendMsg(msg):
    message = client.messages.create(
        #to="+8615622813257",
        to="+8615622813257",
        from_="+18125583488",
        body=msg
)