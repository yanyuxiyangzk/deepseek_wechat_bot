# 在原有导入部分新增
import os
import time
from pprint import pprint

import pyautogui

from Constants import Constants

# 电脑版微信全屏状态的窗口区域
WECHAT_WINDOW = Constants.WECHAT_WINDOW
import easyocr
OCR_READER = easyocr.Reader(['ch_sim', 'en'], gpu=True)  # 添加gpu=True参数启用GPU加速


def extract_text_by_color_flow(image,target_color , tolerance=1):
    """
    修改说明：
    1. 增加区域垂直位置判断逻辑
    2. 返回最下方符合条件的文本区域
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    lower = np.array([max(0, c - tolerance) for c in target_color])
    upper = np.array([min(255, c + tolerance) for c in target_color])
    mask = cv2.inRange(image, lower, upper)

    # 优化轮廓查找参数
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_bottom = -1
    target_contour = None

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        current_bottom = y + h  # 计算区域底部Y坐标

        # 过滤过小区域（根据实际场景调整）
        if w > 50 and h > 20:  # 增加最小宽高限制
            if current_bottom > max_bottom:
                max_bottom = current_bottom
                target_contour = (x, y, w, h)

    return target_contour if target_contour is not None else (0, 0, 0, 0)


import cv2
import numpy as np

# 预定义常量（根据实际场景校准）
GREEN_LOWER = np.array([117, 229, 164])  # BGR颜色下限
GREEN_UPPER = np.array([127, 239, 174])  # BGR颜色上限
X_START = 320  # 水平起始坐标
X_END = 1469  # 水平终止坐标
MIN_Y = 43  # 垂直方向最小检测起点
ROI_HEIGHT = 800  # 感兴趣区域高度


def recognize_green_bottom(image_path):
    """
    性能优化版绿色区域底部检测
    返回：最下方绿色区域的底部Y坐标（全局坐标系），未检测到返回None
    """
    # 闪电加载图像（灰度模式提升读取速度）
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        return None

    try:
        # ROI区域裁剪（减少处理面积）
        h, w = image.shape[:2]
        roi_y1 = max(MIN_Y, 0)
        roi_y2 = min(roi_y1 + ROI_HEIGHT, h)

        # 二次校验防止越界
        if roi_y1 >= h or X_END >= w:
            return None

        roi = image[roi_y1:roi_y2, X_START:X_END]

        # 快速颜色阈值处理
        mask = cv2.inRange(roi, GREEN_LOWER, GREEN_UPPER)

        # 垂直方向投影分析
        vertical_projection = np.any(mask, axis=1)
        y_coords = np.where(vertical_projection)[0]

        if y_coords.size == 0:
            return None

        # 计算全局坐标系Y坐标
        bottom_in_roi = y_coords[-1]  # ROI内的相对Y坐标
        global_y = roi_y1 + bottom_in_roi

        # 有效性验证
        if global_y > h:
            return None

        return int(global_y)

    except Exception as e:
        print(f"检测异常: {str(e)}")
        return None

# 内存缓存优化（减少磁盘IO）
from io import BytesIO

def get_message_area_screenshot():
    screenshot = pyautogui.screenshot(region=msg_area)
    # 直接返回BytesIO对象供后续处理
    img_byte_arr = BytesIO()
    screenshot.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def get_message_area_screenshot():
    # 截取消息区域（根据实际窗口调整）
    msg_area = (
        WECHAT_WINDOW[0] + 304,
        WECHAT_WINDOW[1],
        1479,
        800
    )
    os.makedirs(Constants.MESSAGES_DIR, exist_ok=True)

    screenshot = pyautogui.screenshot(region=msg_area)
    # 生成时间戳文件名
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(
        Constants.MESSAGES_DIR,
        f"{Constants.MESSAGE_PREFIX}{timestamp}.png"
    )
    screenshot.save(screenshot_path)
    return screenshot_path

def preprocess_for_ocr(image):
    """OCR预处理管道"""
    # 灰度化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 自适应阈值二值化
    thresh = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)
    # 降噪处理
    denoised = cv2.fastNlMeansDenoising(thresh, h=10)
    return denoised



def get_chat_messages(screenshot_path):
    """捕获并解析微信消息（带执行时间统计）"""
    total_start = time.time()
    time_stats = {
        'total': 0,
        'image_load': 0,
        'white_detect': 0,
        'green_detect': 0,
        'ocr_process': 0,
        'text_filter': 0
    }
    result = {'white': []}
    try:
        # 图像加载耗时
        img_load_start = time.time()
        image = cv2.imread('./' + screenshot_path)
        time_stats['image_load'] = time.time() - img_load_start

        # 白色区域检测耗时
        white_start = time.time()
        white_target_color = (255, 255, 255)
        bbox = extract_text_by_color_flow(image, white_target_color)
        x, y, w, h = bbox
        time_stats['white_detect'] = time.time() - white_start

        # 绿色区域检测耗时
        green_start = time.time()

        green_target_color = (169, 234, 122)
        green_bbox = extract_text_by_color_flow(image, green_target_color)
        x_green, y_green, w_green, h_green = green_bbox
        # y_green = recognize_green_bottom(screenshot_path)  # 注意参数修正
        time_stats['green_detect'] = time.time() - green_start

        # 区域关系判断
        msg_y_upline = y
        msg_y_downline = y + h
        if y_green and y_green > msg_y_downline:
            print("green区域在消息区域下")
            return result

        # OCR处理耗时
        ocr_start = time.time()
        # OCR_READER = easyocr.Reader(['ch_sim', 'en'])  # 注：初始化建议移到函数外
        processed_img = preprocess_for_ocr(image)

        words_result = OCR_READER.readtext(processed_img)
        time_stats['ocr_process'] = time.time() - ocr_start

        # 文本过滤耗时
        filter_start = time.time()
        clean_text = ''
        for detection in words_result:
            coordinates, text, _ = detection
            upline = coordinates[0][1]
            downline = coordinates[2][1]

            if upline >= msg_y_upline and downline <= msg_y_downline:
                clean_text += text

        if clean_text:
            result['white'].append(clean_text)
        time_stats['text_filter'] = time.time() - filter_start

        # 总耗时计算
        time_stats['total'] = time.time() - total_start

        # 打印耗时分析
        print("\n[性能分析]")
        print(f"总耗时: {time_stats['total']:.3f}s")
        print(
            f"图像加载: {time_stats['image_load'] * 1000:.1f}ms ({time_stats['image_load'] / time_stats['total']:.1%})")
        print(f"白色区域检测: {time_stats['white_detect'] * 1000:.1f}ms")
        print(f"绿色区域检测: {time_stats['green_detect'] * 1000:.1f}ms")
        print(
            f"OCR处理: {time_stats['ocr_process'] * 1000:.1f}ms ({time_stats['ocr_process'] / time_stats['total']:.1%})")
        print(f"文本过滤: {time_stats['text_filter'] * 1000:.1f}ms")

        return result

    except Exception as e:
        print(f"消息捕获失败: {str(e)}")
        return result


# ========== 主程序 ==========
if __name__ == "__main__":
    total_start = time.time()
    image_path = '../pic/message/message_20250224_203547.png'
    result = get_chat_messages(image_path)
    # y = recognize_green_bottom(image_path)
    pprint(result)
    total= time.time() - total_start
    pprint(total)
