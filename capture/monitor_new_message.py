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
    """定位微信新消息红点坐标，返回(x, y)元组"""
    # 闪电加载图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"[预警] 图像加载失败: {image_path}")
        return (None, None)

    # 微信红点特征参数（BGR色彩空间）
    TARGET_COLOR = np.array([88, 94, 231])  # 精确匹配微信消息提示红点
    X_RANGE = (60, 320)  # 有效区域水平坐标范围

    # 生成坐标网格（性能优化关键！）
    x_coords, y_coords = np.meshgrid(
        np.arange(image.shape[1]),
        np.arange(image.shape[0])
    )

    # 构建三维色彩矩阵（比逐像素遍历快100倍）
    color_mask = np.all(image == TARGET_COLOR, axis=-1)
    # 区域智能过滤（排除头像区域和侧边栏干扰）
    region_mask = (x_coords >= X_RANGE[0]) & (x_coords <= X_RANGE[1])

    # 获取所有候选坐标（已自动过滤无效区域）
    matched_points = np.column_stack((
        x_coords[color_mask & region_mask],
        y_coords[color_mask & region_mask]
    ))

    # 智能选择策略：优先取最下方的红点（最新消息）
    if matched_points.size > 0:
        # 按垂直坐标降序排序
        sorted_points = matched_points[np.argsort(-matched_points[:, 1])]
        # 返回首个有效坐标（精确到像素级）
        return tuple(sorted_points[0].astype(int))

    print("[调试] 未检测到有效消息提示")
    return (None, None)





