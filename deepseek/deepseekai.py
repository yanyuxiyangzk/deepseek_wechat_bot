import os

from openai import OpenAI
import re

from db import db
from dotenv import load_dotenv  # 需要先安装python-dotenv

# 在文件开头加载.env文件
load_dotenv()
message_table = {}
my_model = 'deepseek-chat'  # 修改模型名称

client = OpenAI(
    base_url='https://api.deepseek.com/v1',  # 修改API地址
    api_key=os.getenv("DEEPSEEK_API_KEY")  # 替换为真实API密钥
)

def add_user(user_name):
    message_table[user_name] = []

def add_history(user_name, role, content):
    message_table[user_name].append({"role": role, "content": content})

def clean_response(content):
    content = re.sub(r'\[.*?\]', '', content, flags=re.DOTALL)
    # 去除Markdown加粗和倾斜标记
    content = re.sub(r'\*\*\*', '', content)
    content = re.sub(r'\*\*', '', content)
    content = re.sub(r'\*', '', content)
    # 去除行首的#和-
    content = re.sub(r'^\t*[#-]+', '', content, flags=re.MULTILINE)

    content = re.sub(r'\n+', '\n', content)
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
    return content.strip()

def chat(user, prompt):
    db.add_history(user, "user", prompt)
    try:
        response = client.chat.completions.create(
            model=my_model,
            messages=db.get_history(user),
            temperature=0.7,
            top_p=0.9
        )
        # 解析响应保持原有逻辑
        content = response.choices[0].message.content
        content = clean_response(content)
        print(content)
        db.add_history(user, "assistant", content)
        return content
    except Exception as e:
        print(f"DeepSeek API Error: {e}")  # 明确错误来源
        return "服务暂时不可用，请稍后重试"