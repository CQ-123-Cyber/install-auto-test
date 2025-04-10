import os
import re
import shutil
import time
import subprocess
import pygetwindow
import winreg
import pyautogui
from retry import retry

from action.base import InstallTools
from utils.cmd_tools import call_command
from agent.agent import Agent
from utils.screenshot_tools import to_screenshot_b64
from utils.file_tools import handle_remove_read_only


class WindowsInstallTools(InstallTools):
    @staticmethod
    def delete_registry_key():
        try:
            params = (f'Remove-Item -Path "HKLM:\SOFTWARE\WOW6432Node\SEEYON" -Recurse -Force')
            cmd = f"powershell -Command {params}"
            call_command(cmd)
        except:
            pass

    def unzip_package(self):
        dest_dir = self.check_dir
        if os.path.isdir(dest_dir):
            print(f"正在删除上一次的安装包解压目录")
            shutil.rmtree(dest_dir, onerror=handle_remove_read_only)
        unzip_tool_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                       'tools', '7z.exe')
        cmd = f"{unzip_tool_path} x {self.workspace}\\{self.package_name}"
        call_command(cmd, cwd=self.workspace)

    def run_as_admin(self):
        params = (f'Start-Process "{self.workspace}\\{self.package_name.replace(".zip", "")}'
                  f'\\Seeyon{self.product_line}Install.bat" -Verb RunAs')
        cmd = f"powershell -Command {params}"
        call_command(cmd)

    @staticmethod
    # @retry(tries=12, delay=10)
    def get_cmd_window():
        # 获取所有窗口
        titles = pygetwindow.getAllTitles()
        find = False
        for title in titles:
            # jenkins的agent窗口忽略
            if "agent.jar" in title.lower().strip():
                continue
            if title.lower().strip() == "C:\WINDOWS\system32\cmd.exe".lower():
                print("找到了cmd启动窗口")
                find = True
                window = pygetwindow.getWindowsWithTitle(title)[0]
                window.maximize()
                window.restore()
                window.activate()
                time.sleep(3)
                pyautogui.moveTo(window.left + 10, window.top + 10)  # 将鼠标移动到窗口内
                pyautogui.click()  # 执行物理点击确保焦点
                pyautogui.hotkey('enter')  # 比单独press更可靠
        if not find:
            raise RuntimeError('没有找到cmd启动窗口')

    @retry(tries=30, delay=1)
    def get_install_window(self):
        # 获取所有窗口
        titles = pygetwindow.getAllTitles()
        for title in titles:
            # if self.version in title and "安装程序" in title:
            if "安装程序" in title:
                print("找到了InstallAnywhere安装窗口")
                time.sleep(5)  # 等待窗口加载完
                window = pygetwindow.getWindowsWithTitle(title)[0]
                return window

        print("没有找到InstallAnywhere安装窗口，继续点击cmd启动窗口")
        self.get_cmd_window()
        raise RuntimeError('没有找到InstallAnywhere安装窗口')

    # @retry(tries=30, delay=1)
    def get_verify_code_window(self):
        # 获取所有窗口
        titles = pygetwindow.getAllTitles()
        for title in titles:
            if "verify-code.exe" in title:
                print("找到了验证码窗口")
                time.sleep(3)  # 等待窗口加载完
                window = pygetwindow.getWindowsWithTitle(title)[0]
                window.maximize()
                window.restore()
                window.activate()
                return window
        raise RuntimeError('没有找到cmd启动窗口')

    def load_verify_code(self):
        if os.path.isfile(self.verify_code_cache_path):
            with open(self.verify_code_cache_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return None

    def write_verify_code(self):
        with open(self.verify_code_cache_path, 'w', encoding='utf-8') as f:
            f.write(self.verify_code)

    # @retry(tries=5, delay=1)
    def get_verify_code(self):
        verify_code = self.load_verify_code()
        if verify_code:
            return verify_code
        self.run_verify_code()
        time.sleep(5)
        window = self.get_verify_code_window()
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        verify_code_text = Agent.verify_code("识别出验证码", to_screenshot_b64(screenshot))
        window.close()
        pattern = r'\b\d{5}\b'
        matches = re.findall(pattern, verify_code_text)
        if matches:
            self.verify_code = matches[0]
            print(f"验证码：{self.verify_code}")
            self.write_verify_code()
            return self.verify_code
        raise Exception(f"AI获取验证码失败")


if __name__ == "__main__":
    tool = WindowsInstallTools()
    print(tool.delete_registry_key())
