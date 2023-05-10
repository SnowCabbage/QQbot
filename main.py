import asyncio

from function.bingTest import bingRequest
from function.loggerUnit import logger
from function.receiveMsg import rev_msg
from function.sendMsg import send_msg
from function.gptApi import gptRequest

gptRequest = gptRequest()

bingRequest = bingRequest()
asyncio.run(bingRequest.init())

# 防止重复信息
messages = []
id_list = []

while True:
    rev = rev_msg()

    if rev["post_type"] == "message":
        logger.info(rev)

        msgId = rev['message_id']

        if len(id_list) >= 50:
            id_list = []
        print(id_list)
        if msgId not in id_list:
            id_list.append(msgId)
        else:
            continue

        if rev["message_type"] == "private":  # 私聊
            # GPTRequest
            getMsg = gptRequest.getResponse(rev["raw_message"])

            # BingRequest
            # getMsg = asyncio.run(bingRequest.getRequest(rev["raw_message"]))
            # if getMsg == 'Limit':
            #     # bingRequest = bingRequest()
            #     asyncio.run(bingRequest.init())

            qq = rev['sender']['user_id']
            send_msg({'msg_type': 'private', 'number': qq, 'msg': getMsg})
        elif rev["message_type"] == "group":  # 群聊
            group = rev['group_id']
            if "[CQ:at,qq=3185995974]" in rev["raw_message"]:
                # GPTRequest
                getMsg = gptRequest.getResponse(rev["raw_message"].split(" ")[1])

                # BingRequest
                # getMsg = asyncio.run(bingRequest.getRequest(rev["raw_message"]))
                # if getMsg == 'Limit':
                #     # bingRequest = bingRequest()
                #     asyncio.run(bingRequest.init())

                qq = rev['sender']['user_id']
                # logger.info(getMsg)
                print(getMsg)
                send_msg({'msg_type': 'group', 'number': group, 'msg': f'[CQ:at,qq={qq}]' + getMsg})
        else:
            continue
    else:
        continue
