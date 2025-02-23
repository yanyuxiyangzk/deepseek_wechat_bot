# 在原有导入部分新增
import os
import time
from pprint import pprint

import cv2
import numpy as np
import pyautogui

from Constants import Constants

# 电脑版微信全屏状态的窗口区域
WECHAT_WINDOW = Constants.WECHAT_WINDOW

def get_message_area_screenshot():
    # 截取消息区域（根据实际窗口调整）
    msg_area = (
        WECHAT_WINDOW[0] + 304,
        WECHAT_WINDOW[1],
        1479,
        800
    )
    screenshot = pyautogui.screenshot(region=msg_area)
    # 生成时间戳文件名
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(
        Constants.MESSAGES_DIR,
        f"{Constants.MESSAGE_PREFIX}{timestamp}.png"
    )
    screenshot.save(screenshot_path)
    return screenshot_path
def get_chat_messages(screenshot_path):
    """捕获并解析微信消息，返回结构化的消息列表"""
    try:

        import easyocr
        reader = easyocr.Reader(['ch_sim', 'en'])
        words_result = reader.readtext(screenshot_path)
        print(words_result)
        if not words_result:
            print("OCR识别结果为空")
            return []

        result = {'white': []}

        for detection in words_result:

            coordinates, text, confidence = detection
            message = text
            print(message)

            # 提取文字区域坐标
            left = coordinates[0][0]
            top = coordinates[0][1]
            width = coordinates[1][0] - coordinates[0][0]
            height = coordinates[1][1] - coordinates[0][1]
            upline = coordinates[0][1]
            downline = coordinates[2][1]
            print(f"文本内容: {text}")
            print(f"置信度: {confidence:.2f}")
            print(f"坐标位置: {coordinates}")
            print('上线位置: ', upline)
            print('下线位置: ', downline)
            # ============= 新增过滤逻辑 =============
            # 强制过滤left=120的条目到white组
            if left < 125 and upline >= 730 and downline <= 770:
                # clean_text = re.sub(r'[^\u4e00-\u9fa50-9]', '', message)
                clean_text = message
                if clean_text:
                    result['white'].append(clean_text)
                continue  # 跳过后续处理

        return result
    except Exception as e:
        print(f"消息捕获失败: {str(e)}")
        return []

# ========== 主程序 ==========
if __name__ == "__main__":
    image_path = '../pic/message/message_20250223_073551.png'
    result = get_chat_messages(image_path)
    pprint(result)
