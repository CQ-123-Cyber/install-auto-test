import base64
from PIL import Image
from io import BytesIO


def to_screenshot_b64(screenshot):
    # 创建一个 BytesIO 对象来存储图片数据
    buffer = BytesIO()
    # 将截图保存到 BytesIO 对象中，格式为 PNG
    screenshot.save(buffer, format="PNG")
    # 获取字节数据
    image_data = buffer.getvalue()
    # 将字节数据转换为 Base64 编码的字符串
    screenshot_b64 = base64.b64encode(image_data).decode('utf-8')
    # 现在 screenshot_b64 包含 Base64 编码的字符串
    return screenshot_b64


def load_png_to_screenshot_b64(png_path):
    with Image.open(png_path) as image:
        # 创建字节流来保存图片数据
        buffered = BytesIO()
        # 将图片保存到字节流中，格式为 PNG
        image.save(buffered, format="PNG")
        # 获取字节数据
        image_data = buffered.getvalue()
        # 将字节数据转换为 Base64 编码的字符串
        screenshot_b64 = base64.b64encode(image_data).decode('utf-8')
        return screenshot_b64
