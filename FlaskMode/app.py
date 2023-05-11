from flask import Flask, request

from FlaskMode.methods.gptApi import gptRequest
from FlaskMode.methods.loggerUnit import logger
from FlaskMode.methods.sendMsg import sendMsg
from FlaskMode.Info.INFO import image1Url, image2Url

app = Flask(__name__)

import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

idList = []
gptReq = gptRequest()


# '''监听端口，获取QQ信息'''
@app.route('/', methods=["POST"])
def process():
    rev = request.get_json()
    global idList

    url = image2Url

    if rev["post_type"] == "message":

        msgId = rev['message_id']

        if len(idList) >= 50:
            idList = []
        print(idList)
        if msgId not in idList:
            idList.append(msgId)
        else:
            return 'OK', 200
        logger.info(rev)
        if rev["message_type"] == "private":  # 私聊
            # GPTRequest
            getMsg = gptReq.getResponse(rev["raw_message"])

            # Test

            # BingRequest
            # getMsg = asyncio.run(bingRequest.getRequest(rev["raw_message"]))
            # if getMsg == 'Limit':
            #     # bingRequest = bingRequest()
            #     asyncio.run(bingRequest.init())

            qq = rev['sender']['user_id']
            sendMsg({'msg_type': 'private', 'number': qq, 'msg': getMsg})
        elif rev["message_type"] == "group":  # 群聊
            group = rev['group_id']
            if "[CQ:at,qq=3185995974]" in rev["raw_message"]:
                print(rev["raw_message"])
                if rev['sender']['card'] != '':
                    user = rev['sender']['card']
                else:
                    user = rev['sender']['nickname']
                # GPTRequest
                getMsg = gptReq.getResponse(rev["raw_message"].split(" ")[1])

                # Test
                # getMsg = 'GG'

                # BingRequest
                # getMsg = asyncio.run(bingRequest.getRequest(rev["raw_message"]))
                # if getMsg == 'Limit':
                #     # bingRequest = bingRequest()
                #     asyncio.run(bingRequest.init())

                qq = rev['sender']['user_id']
                # logger.info(getMsg)
                print(getMsg)
                sendMsg({'msg_type': 'group', 'number': group, 'msg': f'[CQ:at,qq={qq}]' + getMsg})

    return 'OK', 200


if __name__ == '__main__':
    # 绑定端口,此处port需于config中的url一致
    app.run(debug=False, host='127.0.0.1', port=5701)
