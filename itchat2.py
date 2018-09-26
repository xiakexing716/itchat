# -*- coding=utf-8 -*-
import itchat,time
import re

itchat.auto_login(True)

msg = "Hello, World"
nickrules = re.compile('\d\d[G,M,m,g]{2}[-－_–—～~].*[-－_–—～~].*[-－–—_～~].*[-－–—_～~].*')

friendList = itchat.get_friends(update=True)[1:]
groupList = itchat.get_chatrooms(update=True)
memberList = groupList[0]['MemberList']
nicknames = [item['DisplayName'] for item in memberList]
notrules = [item for item in nicknames if not re.match(nickrules,item) and '非单' not in item]
itchat.send("共有{}个群友的昵称不符合规范".format(notrules),"@@bf052f348f11f883fe9ae703663e6c14fa9ffec5282352e1dbdb006a1f400308")
itchat.send("共有{}个群友的昵称不符合规范".format(len(notrules)),"@@bf052f348f11f883fe9ae703663e6c14fa9ffec5282352e1dbdb006a1f400308")


print(groupList[1])
# print([item['NickName'] for item in groupList])
print([(item['UserName'],item['NickName']) for item in groupList])

itchat.search_chatrooms(userName="@@bf052f348f11f883fe9ae703663e6c14fa9ffec5282352e1dbdb006a1f400308")

# itchat.send("睡觉，晚安","filehelper")
# itchat.send("睡觉，晚安","@@65483da07af535898a470b9cb9aaefac8861d1fb3630af7d460dd4b1ac5c3d2b")
# itchat.send("睡觉，晚安","@@aedebc7d27ec4b31010484391d473aeb4c38861893ca8de411341771c7d3f25d")
# for friend in friendList:
#     print(friend,friend['DisplayName'],friend['NickName'],friend['UserName'])
#     time.sleep(1)
