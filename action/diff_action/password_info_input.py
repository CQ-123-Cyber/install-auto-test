"""定义密码设置界面，适配不同版本和不同产品线"""
import pyautogui
from loguru import logger


class WindowsPasswordInfoInput():
    def __init__(self, install_tool):
        self.install_tool = install_tool

    def action(self, window):
        # 三员分离前
        if self.install_tool.version < 'V8.1':
            return self.lefromv81_a82(window)
        else:
            return self.gtfromv81_a82(window)

    def lefromv81_a82(self, window):
        logger.info(f"password_info_input使用三员分离前")
        position = (459, 103)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 135)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 167)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 195)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 223)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 255)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 287)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 319)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

    def gtfromv81_a82(self, window):
        # 初始化管理员账号
        logger.info(f"password_info_input使用三员分离后")
        position = (459, 103)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('init-admin', interval=0.1)

        position = (459, 135)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 167)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 223)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 255)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 287)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 319)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)


class LinuxPasswordInfoInput():
    def __init__(self, install_tool):
        self.install_tool = install_tool

    def action(self, window):
        # 三员分离前
        if self.install_tool.version < 'V8.1':
            return self.lefromv81_a82(window)
        else:
            return self.gtfromv81_a82(window)

    def lefromv81_a82(self, window):
        logger.info(f"password_info_input使用三员分离前")
        position = (459, 93)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 124)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 153)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 181)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 209)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 237)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 267)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 295)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

    def gtfromv81_a82(self, window):
        # 初始化管理员账号
        logger.info(f"password_info_input使用三员分离后")
        position = (459, 93)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('init-admin', interval=0.1)

        position = (459, 124)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 153)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 209)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 237)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 267)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 295)
        position = self.install_tool.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)
