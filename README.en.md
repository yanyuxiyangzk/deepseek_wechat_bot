# deepseek_wechat_bot

## Description
A WeChat chatbot implemented based on OCR (Optical Character Recognition) and DeepSeek. This chatbot can automatically monitor the WeChat chat window, recognize new messages through OCR technology, and generate intelligent responses using the DeepSeek model.

## Features
- **Automated Message Processing**: Automatically monitors the WeChat chat window and processes new messages.
- **OCR Recognition**: Utilizes the `easyocr` library to perform text recognition on screenshots of WeChat chats and extract chat content.
- **DeepSeek Integration**: Integrates with the DeepSeek model to generate intelligent replies for smart chatting.
- **Flexible Configuration**: Constants such as screenshot saving directories and WeChat window coordinates can be easily adjusted through the configuration file.

## Software Architecture

### Main Modules
- **`Constants.py`**: Defines constants used in the project, such as screenshot saving directories and WeChat window coordinates.
- **`app.py`**: The main application file of the project, containing functions such as message sending and contact loading.
- **`deepseek/deepseekai.py`**: The module that interacts with the DeepSeek API, responsible for sending requests and handling responses.
- **`capture/` Directory**: Contains code related to message capture, processing, and recognition.

### Data Storage
SQLite databases are used to store chat history and message data. The database files include `history.db` and `messages.db`.

### Workflow
1. Monitor the WeChat chat window and automatically take screenshots of the message area when new messages arrive.
2. Use OCR technology to recognize the text content in the screenshots.
3. Send the recognized messages to the DeepSeek model to obtain intelligent replies.
4. Send the reply content to the WeChat chat window.

## Installation

### Clone the Project
```bash
git clone https://github.com/zhangyanhui/deepseek_wechat_bot.git
cd deepseek_wechat_bot
```

### Install Dependencies
This project is written in Python and requires the following dependencies:
```bash
pip install -r requirements.txt
```
The `requirements.txt` file contains all the Python libraries required by the project, such as `pyautogui`, `opencv-python`, `easyocr`, `openai`, etc.

### Configure Environment Variables
Create a `.env` file in the root directory of the project and add the following content:
```plaintext
DEEPSEEK_API_KEY=your_api_key_here
```
Replace `your_api_key_here` with your actual DeepSeek API key.

## Usage

### Start the Program
```bash
python app.py
```

### Configure the Monitoring List
Add the names of the WeChat contacts you want to monitor to the `names.txt` file, with one name per line. For example:
```plaintext
peaceandlove
white
```

### Run Monitoring
After the program starts, it will automatically monitor the WeChat chat window. When new messages arrive, it will automatically process and reply to them.

## Contribution Guide
We welcome developers to contribute code to this project and jointly improve this WeChat chatbot. The specific steps are as follows:

1. Fork the repository.
2. Create a `Feat_xxx` branch, where `xxx` is the name of the feature you want to implement.
3. Develop on the new branch and commit your code.
4. Create a Pull Request and describe your changes and features in detail.

## License
This project is licensed under the [Apache-2.0 license]. For specific terms, please refer to the `LICENSE` file.

## Contact Us
If you encounter any problems during use or have any suggestions or comments, please feel free to contact us through the following methods:

- Email: [yohannzhang@qq.com]
- Issue Feedback: [Link to the project's issue page]