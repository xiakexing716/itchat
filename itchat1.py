# -*- coding=utf-8 -*-
import itchat
import os
import re
import time

msg_dict = {}
rev_tmp_dir = "E:\\桌面临时\\Cache\\itchat"
if not os.path.exists(rev_tmp_dir):
    os.mkdir(rev_tmp_dir)

face_bug = None

@itchat.msg_register(['TEST','PICTURE','MAP','CARD','SHARING','RECORDING','ATTACHMENT','VIDEO','FRIENDS'],isFriendChat=True,isGroupChat=True)
def handler_receive_msg(msg):
    global face_bug
    msg_time_rec = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    msg_id = msg['MsgId']
    msg_time = msg['CreateTime']
    if 'ActualNickName' in msg:
        from_user = msg['ActualUserName']
        msg_from = msg['ActuralNickName']
        friends = itchat.get_friends(update=True)
        for friend in friends:
            if from_user == friend['UserName']:
                if friend['RemarkName']:
                    msg_from = friend['RemarkName']
                else:
                    msg_from = friend['NickName']
                break
        groups = itchat.get_chatrooms(update=True)
        for group in groups:
            if msg['FromUserName'] == group['UserName']:
                group_name = group['NickName']
                group_members = group['MemberCount']
                break
        group_name = group_name + '(' + str(group_members) + ')'

    else:
        if itchat.search_friends(userName=msg['FromUserName'])['RemarkName']:
            msg_from = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']
        else:
            msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
        group_name = ''

    if msg['Type'] in ('Text','Friends'):
        msg_content = msg['Text']
    elif msg['Type'] in ('Recording','Attachment','Video','Picture'):
        msg_content = r'' + msg['FileName']
        msg['Text'](rev_tmp_dir + msg['FileName'] )
    elif msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName'] + r" 的名片"
    elif msg['Type'] == 'Map':
        x,y,location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*",msg['OriContent']).group(1,2,3)
        if location is None:
            msg_content = r"维度->" + x.__str__() + " 经度->" + y.__str__()
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':
        msg_content = msg['Text']
        msg_share_url = msg['Url']
    face_bug = msg_content

@itchat.msg_register('NOTE',isFriendChat=True,isGroupChat=True,isMpChat=True)
def send_msg_helper(msg):
    global face_bug
    if re.search(r"\<\|[CDATA\[.*撤回了一条消息\]\]\>",msg['Content']) is not None:
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>",msg['Content']).group(1)
        old_msg = msg_dict.get(old_msg_id,{})
        if len(old_msg_id) <11:
            itchat.send_file(rev_tmp_dir + face_bug, toUserName="filehelper")
            os.remove(rev_tmp_dir + face_bug)
        else:
            msg_body = "快来看啊，有人撤回消息啦！" + "\n" \
            + old_msg.get('msg_from') + '撤回了' + old_msg.get("msg_type") + " 消息" \
            + "\n" + old_msg.get("msg_time_rec") + "\n" + "撤回什么↓" \
            + r" " + old_msg.get('msg_content')


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()