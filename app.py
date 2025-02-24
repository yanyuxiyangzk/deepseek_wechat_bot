# 在原有导入部分新增
import time
from pprint import pprint
import pyautogui
from capture.deal_chatbox import get_message_area_screenshot, get_chat_messages
from capture.get_name_free import get_friend_name
from capture.monitor_new_message import capture_messages_screenshot, recognize_message
from db import db
from deepseek import deepseekai
import platform

# 新增配置常量
SCREENSHOT_PREFIX = 'wechat_'
WORK_MODE = "forward"  # 模式切换：chat/forward
FORWARD_PREFIX = "[自动转发] "  # 转发模式前缀


def load_config():
    """加载配置文件"""
    try:
        with open('config.cfg', 'r', encoding='utf-8') as f:
            config = {}
            for line in f:
                # 处理带注释的情况
                line = line.split('#')[0].strip()  # 去除注释
                if '=' in line:
                    # 使用split的maxsplit参数防止值含等号
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
            return config.get('mode', 'chat').lower()
    except FileNotFoundError:
        print("⚠️ 配置文件不存在，使用默认chat模式")
        return 'chat'
    except Exception as e:
        print(f"❗ 配置读取失败：{str(e)}，使用默认chat模式")
        return 'chat'



def send_reply(text):
    """发送消息（回车发送方案）"""
    try:
        import pyperclip
        # original = pyperclip.paste()
        pyperclip.copy(text)
        time.sleep(0.3)
        if platform.system() == 'Darwin':
            print('masos')
            pyautogui.hotkey('command', 'a')
            pyautogui.hotkey('command', 'v')
        elif platform.system() == 'Windows':
            print('windows')
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'v')
        else:
            raise Exception("Unsupported OS")
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(0.3)

        # pyperclip.copy(original)
    except Exception as e:
        print(f"发送失败: {str(e)}")
        # pyperclip.copy(original)


def load_contacts():
    """加载监听名单"""
    try:
        with open('names.txt', 'r', encoding='utf-8') as f:
            return [name.strip() for name in f.readlines() if name.strip()]
    except Exception as e:
        print(f"加载联系人失败: {str(e)}")
        return []


if __name__ == "__main__":
    # 初始化配置
    WORK_MODE = load_config()
    listen_list = load_contacts()
    db.create_db()
    db.create_messagesdb()

    print(f"当前模式：{WORK_MODE.upper()} 模式")
    for name in listen_list:
        deepseekai.add_user(name)
        print(f"已监听: {name}")

    while True:
        try:
            screenshot_path = capture_messages_screenshot()
            try:
                x, y = recognize_message(screenshot_path)
                if x is not None and y is not None:
                    print(f"检测到新消息，点击位置: ({x}, {y}) 路径：" + screenshot_path)
                    pyautogui.click(x, y)
                    name = get_friend_name(x, y, screenshot_path)

                    if name not in listen_list:
                        print(f"{name}不在监听列表，跳过处理")
                        continue

                    no_message_count = 0
                    while True:
                        try:
                            screenshot_path = get_message_area_screenshot()
                            final_result = get_chat_messages(screenshot_path)

                            if final_result['white']:
                                latest_msg = final_result['white'][-1]
                                print(f'来自 {name} 的消息：{latest_msg}')

                                # 模式判断逻辑
                                if WORK_MODE == "chat":
                                    reply = deepseekai.chat(name, latest_msg)
                                elif WORK_MODE == "forward":
                                    reply = f"{FORWARD_PREFIX}{latest_msg}"
                                    pyautogui.click(118, 117)
                                # 发送和存储逻辑
                                send_reply(reply)
                                db.save_message(name, latest_msg, reply)
                                print(f"已发送：{reply}")
                                no_message_count = 0
                            else:
                                no_message_count += 1
                                print(f"空消息计数：{no_message_count}/5")

                            if no_message_count >= 5:
                                print("连续5次空消息，退出对话")
                                pyautogui.click(100, 100)
                                break

                            time.sleep(5)
                        except Exception as e:
                            print(f"消息处理异常：{str(e)}")
                            break
            except Exception as e:
                print(f"消息循环异常：{str(e)}")
        except KeyboardInterrupt:
            print("\n程序已终止")
            break
        except Exception as e:
            print(f"运行时错误: {str(e)}")
            time.sleep(5)
