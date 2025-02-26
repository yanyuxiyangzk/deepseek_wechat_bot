import json
import os
import re

import pyautogui
import pyperclip
from dotenv import load_dotenv  # 需要先安装python-dotenv
from openai import OpenAI

from db import db
import time
from time import perf_counter  # 使用更高精度计时器

# 在文件顶部添加性能统计字典
perf_stats = {
    'total': 0.0,
    'api_call': 0.0,
    'response_parse': 0.0,
    'content_clean': 0.0
}
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

def reply(user, msg):
    """带流式响应耗时分析的对话处理"""
    total_start = perf_counter()
    time_stats = {
        'api_call': 0.0,
        'stream_receive': 0.0,
        'content_clean': 0.0,
        'total': 0.0
    }

    try:
        # API调用耗时（包含首包响应时间）
        api_start = perf_counter()
        db.add_history(user, "user", msg)
        thisMsg = db.get_history(user)[-4:]
        #thisMsg 转json 字符串(thisMsg)
        json_msg = json.dumps(thisMsg, ensure_ascii=False)  # 保持中文可读性

        print(json_msg)
        print(thisMsg)
        response = client.chat.completions.create(
            model=my_model,
            messages=[
                {"role": "system", "content": "用尽可能简短（只有几个字或一句话）来回复用户，如果看不懂则调侃用户。"},
                {"role": "user", "content": json_msg}
            ],
            temperature=0.5,
            top_p=0.7,
            max_tokens=384,
            stream=True,
            stream_options={
                "include_usage": False  # 减少返回元数据
            }
        )
        time_stats['api_call'] = perf_counter() - api_start

        # 流式接收耗时
        stream_start = perf_counter()
        content = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                content += chunk.choices[0].delta.content
                pyperclip.copy(chunk.choices[0].delta.content)
                pyautogui.hotkey('command', 'v')
        time_stats['stream_receive'] = perf_counter() - stream_start
        pyautogui.press('enter')

        # 内容清洗耗时
        clean_start = perf_counter()
        cleaned_content = clean_response(content)
        time_stats['content_clean'] = perf_counter() - clean_start

        # 总耗时计算
        time_stats['total'] = perf_counter() - total_start

        # 生成带毫秒的时间戳
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S") + f".{int(time.time() % 1 * 1000):03d}"

        # 打印详细耗时报告
        print(f"\n[API性能报告] {timestamp}")
        print(f"| 阶段            | 耗时(ms)  | 占比   |")
        print("|----------------|-----------|--------|")
        print(
            f"| API首包响应     | {time_stats['api_call'] * 1000:7.1f} | {time_stats['api_call'] / time_stats['total']:6.1%} |")
        print(
            f"| 流式接收        | {time_stats['stream_receive'] * 1000:7.1f} | {time_stats['stream_receive'] / time_stats['total']:6.1%} |")
        print(
            f"| 内容清洗        | {time_stats['content_clean'] * 1000:7.1f} | {time_stats['content_clean'] / time_stats['total']:6.1%} |")
        print(f"| 总耗时          | {time_stats['total'] * 1000:7.1f} | {'100.0%':6} |")

        db.add_history(user, "assistant", cleaned_content)
        return cleaned_content

    except Exception as e:
        # 异常处理
        time_stats['total'] = perf_counter() - total_start
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S") + f".{int(time.time() % 1 * 1000):03d}"

        print(f"\n[API异常] {timestamp}")
        print(f"错误类型: {type(e).__name__}")
        print(f"已耗时: {time_stats.get('total', 0) * 1000:.1f}ms")
        print(f"错误详情: {str(e)}")

        return "服务响应超时，请稍后重试"
