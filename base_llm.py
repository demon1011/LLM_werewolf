import random
from http import HTTPStatus
import dashscope
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0
from config import API_KEY

class base_llm():
    def __init__(self,system_prompt):
        self.api_key=API_KEY
        self.system_prompt=system_prompt
    def call_with_messages(self,prompt_info,temp=0.1):
        #{'role': 'system', 'content': self.system_prompt}
        messages = [{'role': 'user', 'content': prompt_info}]
        dashscope.api_key=self.api_key
        response = Generation.call(model="qwen-plus",
                                   messages=messages,
                                   # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                                   seed=random.randint(1, 10000),
                                   temperature=temp,
                                   # 将输出设置为"message"格式
                                   result_format='message')
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message.content
        else:
            return ('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message))