class Constants:
    """微信机器人配置常量"""

    # 截图配置
    SCREENSHOTS_DIR = 'pic/screenshots'
    MESSAGES_DIR = 'pic/message'

    CHATNAMES_DIR = '../pic/chatname'
    SCREENSHOT_PREFIX = 'wechat_'
    MESSAGE_PREFIX = 'message_'
    CHATNAME_SCREENSHOT_DIR = '../pic/chatname'  # 新增截图保存目录

    # 定义电脑版微信聊天列表的坐标，根据个人电脑调整，可以用微信截图工具查看（微信截图工具坐标原点为左下角，python为右上角，请注意转换）
    # upline ，downlint 每个聊天列表的上边和下边，即x坐标
    # leftline ，rightline 每个聊天列表的左边和右边，即y坐标，leftline从微信头像后算起
    # 以下数据为mac 2022 电脑版微信全屏状态下的数值
    chat_list_eage = [
        {"upline": 24, "downline": 59, "leftline": 116, "rightline": 275},
        {"upline": 100, "downline": 135, "leftline": 116, "rightline": 275},
        {"upline": 176, "downline": 211, "leftline": 116, "rightline": 275},
        {"upline": 252, "downline": 287, "leftline": 116, "rightline": 275},
        {"upline": 328, "downline": 363, "leftline": 116, "rightline": 275},
        {"upline": 404, "downline": 439, "leftline": 116, "rightline": 275},
        {"upline": 480, "downline": 515, "leftline": 116, "rightline": 275},
        {"upline": 556, "downline": 591, "leftline": 116, "rightline": 275},
        {"upline": 632, "downline": 667, "leftline": 116, "rightline": 275},
        {"upline": 708, "downline": 743, "leftline": 116, "rightline": 275},
        {"upline": 784, "downline": 819, "leftline": 116, "rightline": 275}
    ]
    # 微信窗口坐标 (左, 上, 宽, 高)
    WECHAT_WINDOW = (0, 0, 1479, 956)
    WECHAT_FRIEND_WINDOW = (0, 0, 320, 956)

    # 消息区域裁剪参数
    CROP_REGION = (55, 55 + 40, 320, 320 + 1000)  # (y_start, y_end, x_start, x_end)

    # 其他业务参数
    MAX_RETRY = 3
    POLLING_INTERVAL = 5  # 秒
