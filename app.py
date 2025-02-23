# 在原有导入部分新增

import time

from pprint import pprint
import pyautogui


from capture.deal_chatbox import get_message_area_screenshot, get_chat_messages
from capture.get_name_free import get_friend_name
from capture.monitor_new_message import capture_messages_screenshot, recognize_message
from db import db
from deepseek import deepseekai

SCREENSHOT_PREFIX = 'wechat_'   # 文件名前缀
def send_reply(text):
    """发送消息（回车发送方案）"""
    try:
        import pyperclip

        # 备份剪贴板
        original = pyperclip.paste()
        pyperclip.copy(text)

        # 执行粘贴
        # pyautogui.click(INPUT_BOX)
        time.sleep(0.3)
        pyautogui.hotkey('command', 'a')  # 全选清除历史内容
        pyautogui.hotkey('command', 'v')  # 粘贴
        time.sleep(0.2)

        # 发送消息
        pyautogui.press('enter')  # 回车发送
        time.sleep(0.3)

        # 恢复剪贴板
        pyperclip.copy(original)

    except Exception as e:
        print(f"发送失败: {str(e)}")
        pyperclip.copy(original)
def load_contacts():
    """加载监听名单"""
    try:
        with open('names.txt', 'r', encoding='utf-8') as f:
            return [name.strip() for name in f.readlines() if name.strip()]
    except Exception as e:
        print(f"加载联系人失败: {str(e)}")
        return []

# ========== 主程序 ==========
if __name__ == "__main__":
    # 首次运行建议执行校准
    # calibrate()
    # 初始化
    listen_list = load_contacts()
    db.create_db()
    db.create_messagesdb()

    # 注册监听用户
    for name in listen_list:
        deepseekai.add_user(name)
        print(f"已监听: {name}")

    # 主循环
    while True:
        try:
            screenshot_path = capture_messages_screenshot()
            # screenshot_path = 'screenshots/wechat_20250221_202332.png'
            try:
                # 监测红点，识别消息位置
                x, y = recognize_message(screenshot_path)
                #打印x,y
                if x is not None and y is not None:

                    print(f"检测到新消息，点击位置: ({x}, {y}) 路径："+screenshot_path)
                    pyautogui.click(x, y)
                    name = get_friend_name(x,y,screenshot_path)
                    print(name)
                    #判断name是否在listen_list中，若不是，跳过处理
                    if name not in listen_list:
                        print(f"{name}不在监听列表，跳过处理")
                        continue


                    no_message_count = 0  # 新增计数器变量
                    # 修改后的主循环部分
                    while True:
                        try:
                            screenshot_path = get_message_area_screenshot()
                            print('当前截图路径：'+screenshot_path)


                            final_result = get_chat_messages(screenshot_path)
                            pprint(final_result)
                            # 消息处理逻辑
                            has_new_message = False  # 新增消息存在标志
                            # 取白色区域最后一条结果
                            if final_result['white']:
                                latest_msg = final_result['white'][-1]
                                print('来自朋友：' + name + ' 的最新一条消息：' + latest_msg)
                                if latest_msg and name in listen_list:
                                    # 发送回复（示例逻辑）
                                    reply = deepseekai.chat(name, latest_msg)
                                    send_reply(reply)
                                    db.save_message(name, latest_msg, reply)
                                    print(f"已发送回复: {reply}")
                                    has_new_message = True  # 标记有消息
                                else:
                                    print("未识别到消息")
                            else:
                                print("白色区域结果为空")
                            # 计数器逻辑
                            if not has_new_message:
                                no_message_count += 1
                                print(f"无新消息计数: {no_message_count}/5")
                                if no_message_count >= 5:
                                    print("连续5次无新消息，跳出循环")
                                    pyautogui.click(100, 100)
                                    break
                            else:
                                no_message_count = 0  # 重置计数器
                        finally:
                            print("循环结束")
                        time.sleep(5)
            except Exception as e:
                print(f"处理失败：{str(e)}")
        except KeyboardInterrupt:
            print("\n程序已终止")
            break

        except Exception as e:
            print(f"运行时错误: {str(e)}")
            time.sleep(5)