# 在原有导入部分新增
import os
import random
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
WORK_MODE = "chat"  # 模式切换：chat/forward
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


from PIL import Image
import io
import platform


def copy_image_to_clipboard(image_path):
    system = platform.system()
    img = Image.open(image_path)

    if system == "Darwin":  # macOS
        from AppKit import NSPasteboard, NSImage
        nsimage = NSImage.alloc().initWithContentsOfFile_(image_path)
        NSPasteboard.generalPasteboard().clearContents()
        NSPasteboard.generalPasteboard().writeObjects_([nsimage])

    elif system == "Windows":  # Windows
        import win32clipboard
        output = io.BytesIO()
        img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]  # 去除BMP头
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    elif system == "Linux":  # Linux
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk, Gdk
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_image(Gtk.Image.new_from_file(image_path).get_pixbuf())
        clipboard.store()


def send_image(image_path):
    """发送图片文件（适用于微信桌面端）"""
    try:
        import pyperclip
        # 保存原始剪贴板内容
        original = pyperclip.paste()

        # 激活附件按钮（坐标需根据实际界面调整）
        # pyautogui.click(x=130, y=680)  # 微信附件按钮坐标

        time.sleep(1)  # 等待文件选择框打开

        # 输入绝对路径（需要处理不同操作系统路径格式）
        if platform.system() == 'Windows':
            image_path = os.path.abspath(image_path).replace('/', '\\')
        else:
            image_path = os.path.abspath(image_path)

        # pyperclip.copy(image_path)
        copy_image_to_clipboard(image_path)
        time.sleep(0.5)

        # 粘贴路径并确认（Windows/Mac不同热键）
        if platform.system() == 'Darwin':
            pyautogui.hotkey('command', 'v')
            time.sleep(0.5)
            pyautogui.press('enter')
        else:
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.press('enter', presses=2)  # 需要两次回车

        time.sleep(1)
        # 恢复剪贴板内容
        pyautogui.copy(original)
    except Exception as e:
        print(f"图片发送失败: {str(e)}")


def send_reply(text):
    """发送消息（回车发送方案）"""
    try:
        import pyperclip

        if platform.system() == 'Darwin':
            print('masos')
            pyperclip.copy(text)
            # pyautogui.typewrite(text, interval=0.1)  # 模拟打字
            pyautogui.hotkey('command', 'a')
            pyautogui.hotkey('command', 'v')
        elif platform.system() == 'Windows':
            print('windows')
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'v')
        else:
            raise Exception("Unsupported OS")
        time.sleep(0.1)
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
                    #
                    pyautogui.moveTo(x, y, duration=random.uniform(0.2, 0.5))  # 随机移动速度
                    pyautogui.click(x, y)
                    screenshot_path = capture_messages_screenshot()
                    name = get_friend_name(x, y, screenshot_path)

                    if name not in listen_list:
                        print(f"{name}不在监听列表，跳过处理")
                        continue

                    no_message_count = 0
                    while True:
                        try:
                            screenshot_path = get_message_area_screenshot()
                            final_result = get_chat_messages(screenshot_path)
                            pprint(final_result)

                            if final_result['white']:
                                latest_msg = final_result['white'][-1]
                                print(f'来自 {name} 的消息：{latest_msg}')

                                # 模式判断逻辑
                                if WORK_MODE == "chat":
                                    reply = deepseekai.reply(name, latest_msg)
                                elif WORK_MODE == "forward":
                                    reply = f"{FORWARD_PREFIX}{latest_msg}"
                                    pyautogui.click(118, 117)
                                    send_image(screenshot_path)
                                    send_reply(reply)
                                    # send_reply('@')
                                    # time.sleep(0.1)
                                # 发送和存储逻辑
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
                            time.sleep(1)
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
