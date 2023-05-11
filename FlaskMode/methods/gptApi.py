import requests
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt

from FlaskMode.Info.INFO import gptApiKey
from FlaskMode.methods.loggerUnit import logger

openai.api_key = gptApiKey

headers = {'Authorization': 'Bearer ' + gptApiKey,
           'content-type': 'application/json'}  # 设置请求头
url = 'https://api.openai.com/v1/chat/completions'
data = {
    "model": "gpt-3.5-turbo",
    "messages": [],
    "temperature": 0.7
}
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}


class gptRequest():
    messages = []

    @retry(wait=wait_random_exponential(min=18, max=60), stop=stop_after_attempt(10))
    def getResponse(self, msg):
        logger.info(msg)

        self.messages.append({'role': 'user', 'content': msg})
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.messages,
        )

        print(response)
        # logger.info(response)
        ans = response['choices'][0]['message']['content']
        self.messages.append({
            "role": "assistant",
            "content": ans
        })
        return ans
        # return response.get('content')


if __name__ == '__main__':
    gptRequest = gptRequest()
    print(gptRequest.getResponse('你会游泳吗'))
