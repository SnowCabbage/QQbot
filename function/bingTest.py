import asyncio
from EdgeGPT import Chatbot, ConversationStyle


class bingRequest():

    def __init__(self):
        self.cnt = 1
        self.bot = Chatbot

    async def init(self):
        self.bot = await Chatbot.create(cookie_path='./function/cookies.json')
        self.cnt = 1

    async def getRequest(self, msg):
        if self.cnt == 20:
            return "Limit"
        response = await self.bot.ask(prompt=msg, conversation_style=ConversationStyle.balanced,
                                      wss_link="wss://sydney.bing.com/sydney/ChatHub")
        self.cnt += 1
        return response['item']['messages'][1]['text']


if __name__ == "__main__":
    bingRequest = bingRequest()
    asyncio.run(bingRequest.init())
    while True:
        msg = input('Enter:')
        if msg == 'exit':
            break
        print(asyncio.run(bingRequest.getRequest(msg)))
