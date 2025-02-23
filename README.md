
```markdown
# deepseek_wechat_bot

基于OCR（光学字符识别）和DeepSeek实现的微信聊天机器人，通过自动化截图、OCR识别以及与DeepSeek模型的交互，实现智能的微信聊天功能。

## 功能特性

- **自动化消息处理**：自动监控微信聊天窗口，识别新消息并进行处理。
- **OCR识别**：利用 `easyocr` 库对微信聊天截图进行文字识别，提取聊天内容。
- **DeepSeek集成**：借助DeepSeek模型生成智能回复，实现智能聊天。
- **配置灵活**：通过常量配置文件，可以方便地调整截图区域、窗口坐标等参数。

## 软件架构

### 主要模块
- **`Constants.py`**：定义项目中使用的常量，如截图保存目录、微信窗口坐标等。
- **`app.py`**：项目的主应用程序文件，包含消息发送、联系人加载等功能。
- **`deepseek/deepseekai.py`**：与DeepSeek API交互的模块，负责发送请求、处理响应。
- **`capture/` 文件夹**：包含消息捕获、处理和识别的相关代码。

### 数据存储
使用SQLite数据库存储聊天历史记录和消息数据，数据库文件包括 `history.db` 和 `messages.db`。

### 工作流程
1. 监控微信聊天窗口，当有新消息时，自动截取消息区域的屏幕截图。
2. 使用OCR技术识别截图中的文字内容。
3. 将识别到的消息发送给DeepSeek模型，获取智能回复。
4. 将回复内容发送到微信聊天窗口。

## 安装步骤

### 克隆项目
```bash
git clone <项目仓库地址>
cd deepseek_wechat_bot
```

### 安装依赖
项目使用Python编写，需要安装以下依赖库：
```bash
pip install -r requirements.txt
```
`requirements.txt` 文件中包含了项目所需的所有Python库，如 `pyautogui`、`opencv-python`、`easyocr`、`openai` 等。

### 配置环境变量
在项目根目录下创建 `.env` 文件，并添加以下内容：
```plaintext
DEEPSEEK_API_KEY=your_api_key_here
```
将 `your_api_key_here` 替换为你的DeepSeek API密钥。

## 使用方法

### 启动程序
```bash
python app.py
```

### 配置监听名单
在 `names.txt` 文件中添加需要监听的微信联系人名称，每行一个名称。例如：
```plaintext
peaceandlove
white
```

### 运行监控
程序启动后，会自动监控微信聊天窗口，当有新消息时，会自动进行处理并回复。

## 贡献指南

欢迎各位开发者为项目贡献代码，共同完善这个微信聊天机器人。具体步骤如下：

1. Fork 仓库。
2. 创建 `Feat_xxx` 分支，其中 `xxx` 为你要实现的功能名称。
3. 在新分支上进行开发，提交你的代码。
4. 创建 Pull Request，详细描述你的改动和功能。

## 许可证
本项目使用 [Apache-2.0 license] 许可证，具体条款请参考 `LICENSE` 文件。

## 联系我们
如果你在使用过程中遇到任何问题，或者有任何建议和意见，欢迎通过以下方式联系我们：

- 邮箱：[yohannzhang@qq.com]
- 问题反馈：[项目的issue页面链接]
```
