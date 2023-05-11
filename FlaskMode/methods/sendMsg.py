from urllib import parse

import requests

from function.constInfo import MyQQ, TESTId

baseUrl = 'http://127.0.0.1:5700/'


def sendMsg(resp_dict):
    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    number = resp_dict['number']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息

    # 将字符中的特殊字符进行url编码
    msg = parse.quote(msg)

    payload = ""

    if msg_type == 'group':
        payload = baseUrl + 'send_group_msg?group_id={0}&message={1}'.format(number, msg)
    elif msg_type == 'private':
        payload = baseUrl + 'send_private_msg?user_id={0}&message={1}'.format(number, msg)
    print("发送" + payload)
    requests.get(url=payload)
    return 'OK'


resp_dict1 = {'msg_type': 'private', 'number': MyQQ,
              'msg': 'Rothschild & Co. 是一家历史悠久的国际金融服务公司，创立于1760年'}
resp_dict2 = {'msg_type': 'group', 'number': TESTId, 'msg': f'[CQ:at,qq={MyQQ}]'}
resp_dict3 = {'msg_type': 'group', 'number': TESTId, 'msg': '[CQ:face,id=132]'}
if __name__ == '__main__':
    sendMsg(resp_dict1)
