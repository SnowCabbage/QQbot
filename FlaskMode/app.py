from flask import Flask, request
from jinja2 import environment

from FlaskMode.methods.gptApi import gptRequest
from FlaskMode.methods.loggerUnit import logger
from FlaskMode.methods.sendMsg import sendMsg

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

    if rev["post_type"] == "message":

        msgId = rev['message_id']

        if len(idList) >= 50:
            idList = []
        print(idList)
        if msgId not in idList:
            idList.append(msgId)
        else:
            return 'OK'
        logger.info(rev)
        if rev["message_type"] == "private":  # 私聊
            # GPTRequest
            getMsg = gptReq.getResponse(rev["raw_message"])

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
                # GPTRequest
                getMsg = gptReq.getResponse(rev["raw_message"].split(" ")[1])

                # BingRequest
                # getMsg = asyncio.run(bingRequest.getRequest(rev["raw_message"]))
                # if getMsg == 'Limit':
                #     # bingRequest = bingRequest()
                #     asyncio.run(bingRequest.init())

                qq = rev['sender']['user_id']
                # logger.info(getMsg)
                print(getMsg)
                sendMsg({'msg_type': 'group', 'number': group, 'msg': f'[CQ:at,qq={qq}]' + getMsg})

    return 'OK'


if __name__ == '__main__':
    # 绑定端口,此处port需于config中的url一致
    app.run(debug=False, host='127.0.0.1', port=5701)
