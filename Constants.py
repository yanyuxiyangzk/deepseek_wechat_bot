class Constants:
    """微信机器人配置常量"""

    # 截图配置
    SCREENSHOTS_DIR = 'pic/screenshots'
    MESSAGES_DIR = 'pic/message'

    CHATNAMES_DIR = 'pic/chatname'
    SCREENSHOT_PREFIX = 'wechat_'
    MESSAGE_PREFIX = 'message_'
    CHATNAME_SCREENSHOT_DIR = 'pic/chatname'  # 新增截图保存目录

    # 定义电脑版微信聊天列表的坐标，根据个人电脑调整，可以用微信截图工具查看（微信截图工具坐标原点为左下角，python为右上角，请注意转换）
    # upline ，downlint 每个聊天列表的上边和下边，即x坐标
    # leftline ，rightline 每个聊天列表的左边和右边，即y坐标，leftline从微信头像后算起
    # 以下数据为mac 2022 电脑版微信全屏状态下的数值
    chat_list_eage = [
    {"upline": 111    ,"downline": 133, "leftline": 116, "rightline": 275},
    {"upline": 186    ,"downline": 208, "leftline": 116, "rightline": 275},
    {"upline": 261    ,"downline": 283, "leftline": 116, "rightline": 275},
    {"upline": 336    ,"downline": 358, "leftline": 116, "rightline": 275},
    {"upline": 411    ,"downline": 433, "leftline": 116, "rightline": 275},
    {"upline": 486    ,"downline": 508, "leftline": 116, "rightline": 275},
    {"upline": 561    ,"downline": 583, "leftline": 116, "rightline": 275},
    {"upline": 636    ,"downline": 658, "leftline": 116, "rightline": 275},
    {"upline": 711    ,"downline": 733, "leftline": 116, "rightline": 275},
    {"upline": 786    ,"downline": 808, "leftline": 116, "rightline": 275},
    {"upline": 861    ,"downline": 883, "leftline": 116, "rightline": 275}
    ]
    # 微信窗口坐标 (左, 上, 宽, 高)
    WECHAT_WINDOW = (0, 0, 1479, 956)
    WECHAT_FRIEND_WINDOW = (0, 0, 320, 956)

    # 消息区域裁剪参数
    CROP_REGION = (55, 55 + 40, 320, 320 + 1000)  # (y_start, y_end, x_start, x_end)

    # 其他业务参数
    MAX_RETRY = 3
    POLLING_INTERVAL = 5  # 秒
