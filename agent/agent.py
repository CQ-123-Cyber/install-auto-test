import requests
import json

url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
api_key = "sk-d1b82892759b4feba984b823b79a3a5a"
model = "deepseek-r1"


url = f"https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
api_key = "sk-af877d0ab744453eaa437da0df76eeaa"
model = "qwen-vl-plus"
model = "qvq-72b-preview"  # 只支持单轮对话
model = "qwen-vl-max-2025-01-25"  # 图片+推理效果不好
# model = "llama-4-maverick-17b-128e-instruct"
# model = "qwen2.5-vl-32b-instruct" # 图片+推理效果不好
# model = 'qwen-vl-ocr'


class Agent:
    @staticmethod
    def verify(task, screenshot):
        print(f"正在AI验证的task：{task}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        # 定义要发送的数据
        data = {
            "messages": [
                {
                    "content": "你是一个安装程序测试助手",
                    "role": "system"},
                {
                    "content": """
你的任务是根据图片判断操作之后，当前的窗口是否正确，返回格式json，示例：
{"status": "正确", "explain": ""}
或者
{"status": "不正确", "explain": ""}
注意只返回json的内容
                    """,
                    "role": "user"
                },
                {"content": [
                    {'type': 'text', 'text': task},
                    {
                        'type': 'image_url',
                        'image_url': {'url': f'data:image/png;base64,{screenshot}'},
                    },
                ],

                    "role": "user"}
            ],
            "model": model,
            # "type": "json_object"
        }

        res = requests.post(url, headers=headers, json=data, timeout=600)
        print(res.text)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            content = content.replace("```json", "").replace("```", "")
            return json.loads(content)
        return None

    @staticmethod
    def check_from_base(task, screenshot, base_screenshot):
        print(f"正在AI对比检查的task：{task}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        # 定义要发送的数据
        data = {
            "messages": [
                {
                    "content": "你是一个安装程序测试助手",
                    "role": "system"},
                {
                    "content": """
你的任务是以正确的窗口截图为基准，判断当前的安装窗口是否正确，2次比较除了版本号和安装输入内容之外，其他需要保持一致，返回格式json，示例：
{"status": "正确", "explain": ""}
或者
{"status": "不正确", "explain": ""}
注意检查当前安装窗口的文字说明是否有误
注意只返回json的内容
                    """,
                    "role": "user"
                },
                {
                    "content": [
                        {'type': 'text', 'text': '这是正确的基准窗口截图'},
                        {
                            'type': 'image_url',
                            'image_url': {'url': f'data:image/png;base64,{base_screenshot}'},
                        },
                    ],
                    "role": "user"
                },
                {
                    "content": [
                        {'type': 'text', 'text': '这是需要判断的当前窗口截图'},
                        {
                            'type': 'image_url',
                            'image_url': {'url': f'data:image/png;base64,{screenshot}'},
                        },
                    ],
                    "role": "user"
                }
            ],
            "model": model,
        }

        res = requests.post(url, headers=headers, json=data, timeout=600)
        print(res.text)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            content = content.replace("```json", "").replace("```", "")
            return json.loads(content)
        return None

    @staticmethod
    def check(task, screenshot):
        print(f"正在AI检查的task：{task}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        # 定义要发送的数据
        data = {
            "messages": [
                {
                    "content": "你是一个安装程序测试助手",
                    "role": "system"},
                {
                    "content": """
你的任务是检查安装程序当前窗口是否符合断言：%s，图片完全符合断言才返回正确，否则返回不正确，
返回格式json，示例：
{"status": "正确", "explain": ""}
或者
{"status": "不正确", "explain": ""}
注意只返回json的内容
                    """ % task,
                    "role": "user"
                },
                {
                    "content": [
                        {'type': 'text', 'text': '这是需要判断的当前窗口截图'},
                        {
                            'type': 'image_url',
                            'image_url': {'url': f'data:image/png;base64,{screenshot}'},
                        },
                    ],
                    "role": "user"
                }
            ],
            "model": model,
        }

        res = requests.post(url, headers=headers, json=data, timeout=600)
        print(res.text)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            content = content.replace("```json", "").replace("```", "")
            return json.loads(content)
        return None

    @staticmethod
    def help(task, screenshot):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        # 定义要发送的数据
        data = {
            "messages": [
                {
                    "content": "你是一个安装程序测试助手",
                    "role": "system"},
                {
                    "content": """
你的任务是根据图片用python脚本帮助完成任务
                    """,
                    "role": "user"
                },
                {"content": [
                    {'type': 'text', 'text': task},
                    {
                        'type': 'image_url',
                        'image_url': {'url': f'data:image/png;base64,{screenshot}'},
                    },
                ],

                    "role": "user"}
            ],
            "model": model,
            # "type": "json_object"
        }

        res = requests.post(url, headers=headers, json=data, timeout=600)
        print(res.text)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            content = content.replace("```json", "").replace("```", "")
            return json.loads(content)
        return None

    @staticmethod
    def language(task, screenshot):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        # 定义要发送的数据
        data = {
            "messages": [
                {
                    "content": "你是一个windows助手",
                    "role": "system"},
                {
                    "content": """
你的任务是根据图片识别当前系统使用的输入法是中文还是英文
注意，只返回中文或者英文
                    """,
                    "role": "user"
                },
                {"content": [
                    {'type': 'text', 'text': task},
                    {
                        'type': 'image_url',
                        'image_url': {'url': f'data:image/png;base64,{screenshot}'},
                    },
                ],

                    "role": "user"}
            ],
            "model": model,
            # "type": "json_object"
        }

        res = requests.post(url, headers=headers, json=data, timeout=600)
        print(res.text)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            return content
        return None

    @staticmethod
    def verify_code(task, screenshot):
        url = f"https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        api_key = "sk-af877d0ab744453eaa437da0df76eeaa"
        model = 'qwen-vl-ocr'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        # 定义要发送的数据
        data = {
            "messages": [
                {
                    "content": "你是一个图片识别助手",
                    "role": "system"},
                {
                    "content": """
你的任务是根据图片识别当前出验证码，验证码是窗口中只包含数字那行
注意，只返回验证码
                    """,
                    "role": "user"
                },
                {"content": [
                    {'type': 'text', 'text': task},
                    {
                        'type': 'image_url',
                        'image_url': {'url': f'data:image/png;base64,{screenshot}'},
                    },
                ],

                    "role": "user"}
            ],
            "model": model,
            # "type": "json_object"
        }

        res = requests.post(url, headers=headers, json=data, timeout=600)
        print(res.text)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            return content
        return None