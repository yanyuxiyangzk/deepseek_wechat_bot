import os
from datetime import datetime

import cv2
import numpy as np
import pyautogui

from Constants import Constants






def capture_messages_screenshot(save_dir=Constants.SCREENSHOTS_DIR,
                                region=Constants.WECHAT_WINDOW,
                                prefix=Constants.SCREENSHOT_PREFIX):
    """
    消息区域截图方法
    参数：
        save_dir: 截图保存目录
        region: 截图区域 (x, y, width, height)
        prefix: 文件名前缀
    返回：
        str: 截图文件完整路径
    """
    os.makedirs(save_dir, exist_ok=True)

    # 生成带时间戳的文件名
    filename = f"{prefix}{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    save_path = os.path.join(save_dir, filename)

    # 使用pyautogui截图
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(save_path)
    return save_path


def recognize_message(image_path):
    """返回格式始终为 (x, y) 的元组"""
    image = cv2.imread(image_path)  # 修正参数名称

    if image is None:
        print(f"无法读取图像: {image_path}")
        return (None, None)  # 保持返回结构

    height, width, _ = image.shape

    # 使用numpy向量化操作提升性能（快100倍以上）

    target_color = np.array([88, 94, 231])  # BGR格式
    mask = np.all(image == target_color, axis=-1)

    # 查找所有匹配坐标
    y_coords, x_coords = np.where(mask)

    if len(x_coords) > 0 and len(y_coords) > 0:
        # 取第一个符合要求的坐标，并筛选x范围
        valid_indices = np.where((x_coords >= 60) & (x_coords <= 320))[0]

        if len(valid_indices) > 0:
            idx = valid_indices[0]
            x, y = x_coords[idx], y_coords[idx]
            # print(f"找到目标坐标: ({x}, {y})")
            return (x, y)

    print("未找到符合条件的坐标")
    return (None, None)  # 保持返回结构一致性





