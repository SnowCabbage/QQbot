import socket

from function.constInfo import TESTId, MyQQ


def send_msg(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1'
    client.connect((ip, 5700))

    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    number = resp_dict['number']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息

    # 将字符中的特殊字符进行url编码
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")
    msg = msg.replace("&", "%26")

    payload = ""

    if msg_type == 'group':
        payload = "GET /send_group_msg?group_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    elif msg_type == 'private':
        payload = "GET /send_private_msg?user_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0


resp_dict1 = {'msg_type': 'private', 'number': MyQQ, 'msg': 'Rothschild & Co. 是一家历史悠久的国际金融服务公司，创立于1760年'}
resp_dict2 = {'msg_type': 'group', 'number': TESTId, 'msg': f'[CQ:at,qq={MyQQ}]'}
resp_dict3 = {'msg_type': 'group', 'number': TESTId, 'msg': '[CQ:face,id=132]'}
if __name__ == '__main__':
    send_msg(resp_dict1)
