# -*- coding=utf-8 -*-
import itchat,time
from itchat.content import TEXT
from itchat.content import *
import re

@itchat.msg_register(NOTE,isGroupChat=True)
def receive_red_packet(msg):
    if "收到红包" in msg['Content']:
        groups = itchat.get_chatrooms(update=True)
        # users = itchat.search_chatrooms(name='')
        # username = users[0]['UserName']
        for g in groups:
            if msg['FromUserName'] == g['UserName']:
                group_name = g['NickName']
        msgbody = "有人在群%s发了红包，请立即打电话给我，让我去抢" % group_name
        itchat.send(msgbody,toUserName='filehelper')

itchat.auto_login(True)
itchat.run()

