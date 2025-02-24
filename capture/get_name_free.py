# 定义数据结构
import os

import cv2
import easyocr

from Constants import Constants
from capture.monitor_new_message import recognize_message

import easyocr
OCR_READER = easyocr.Reader(['ch_sim', 'en'], gpu=True)  # 添加gpu=True参数启用GPU加速
def get_chat_name(image_path, screenshot_dir=Constants.CHATNAME_SCREENSHOT_DIR, crop_region=(55, 55+40, 320, 320+1000)):
    """
    处理微信截图并执行OCR识别
    参数：
        image_path: 原始图片路径
        screenshot_dir: 截图保存目录
        crop_region: 裁剪区域元组 (y_start, y_end, x_start, x_end)
    返回：
        list: 识别的文字结果列表
    """
    # 读取并裁剪图像
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"无法读取图像文件：{image_path}")

    y_start, y_end, x_start, x_end = crop_region
    cropped_image = image[y_start:y_end, x_start:x_end]

    # 保存临时文件
    os.makedirs(screenshot_dir, exist_ok=True)  # 确保截图目录存在
    cropped_path = os.path.join(screenshot_dir, 'cropped_' + os.path.basename(image_path))
    cv2.imwrite(cropped_path, cropped_image)

    # reader = easyocr.Reader(['ch_sim', 'en'])
    result = OCR_READER.readtext(cropped_image)
    if not result:
        print("OCR识别结果为空")
        return []

    texts = [item[1] for item in result]
    print(texts[0])

    return texts[0]


def get_friend_name(x,y,image_path):
    # 添加空值检查
    if x is not None and y is not None:

        # 遍历数据，判断坐标是否在某个区间内
        for item in Constants.chat_list_eage:
            if item["upline"] <= y <= item["downline"]:
                print(
                    f"坐标 ({x}, {y}) 在区间 [{item['upline']}, {item['downline']}] 和 [{item['leftline']}, {item['rightline']}] 内")
                x = item['leftline']
                y = item['upline']
                w = item['rightline'] - item['leftline']
                h = item['downline'] - item['upline']
                crop_region = (x, y, w, h)
                print(crop_region)
                # 使用示例
                name = get_chat_name(
                    image_path,
                    crop_region=(y, y + h, x, x + w)  # y_start=55, height=40, x_start=320, width=1000
                )
                return name
                break
        else:
            print(f"坐标 ({x}, {y}) 不在任何区间内")

# ========== 主程序 ==========
if __name__ == "__main__":
    # 给定的坐标
    path = '/Users/yanhuizhang/PycharmProjects/deep-seek-wechat/screenshots/wechat_20250223_041932.png'
    x,y = recognize_message(path)
    name = get_friend_name(x,y,path)
    # print(name)
