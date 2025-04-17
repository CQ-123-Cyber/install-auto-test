import os
import yaml
import shutil
import time
import pygetwindow
import pyautogui
from retry import retry
from loguru import logger

from action.base import InstallTools
from utils.cmd_tools import call_command
from agent.agent import Agent
from utils.screenshot_tools import to_screenshot_b64
from utils.file_tools import handle_remove_read_only
from action.check_list.windows_check_list import WindowsCheckList
from action.check_list.no_check_list import NoCheckList
from utils.time_help import datetime2str_by_format


class WindowsInstallTools(InstallTools):
    def __init__(self):
        super().__init__()
        self.check_list = WindowsCheckList(self) if self.is_check_list == True else NoCheckList(self)

    def delete_install_path(self):
        if os.path.isdir(self.install_path):
            shutil.rmtree(self.install_path, onerror=handle_remove_read_only)

    @staticmethod
    def delete_registry_key():
        try:
            params = (f'Remove-Item -Path "HKLM:\SOFTWARE\WOW6432Node\SEEYON" -Recurse -Force')
            cmd = f"powershell -Command {params}"
            call_command(cmd)
        except:
            pass

    def download(self):
        """下载安装程序"""
        cmd = f"curl {self.package_download_url} -o {self.install_workspace}/{self.package_name}"
        call_command(cmd)

    def unzip_package(self):
        dest_dir = self.check_dir
        if os.path.isdir(dest_dir):
            logger.info(f"正在删除上一次的安装包解压目录")
            shutil.rmtree(dest_dir, onerror=handle_remove_read_only)
        unzip_tool_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                       'tools', '7z.exe')
        cmd = f"{unzip_tool_path} x {self.install_workspace}\\{self.package_name}"
        call_command(cmd, cwd=self.install_workspace)

    def change_check_config(self):
        """修改安装检查项"""
        check_yaml_path = os.path.join(self.check_dir, 'inst', 'check.yml')
        if os.path.isfile(check_yaml_path):
            self.change_check_config_file(check_yaml_path)
            print("修改完成，warningMemoryMb 已更改为 0")
        else:
            logger.info(f"没有找到修改安装检查项的配置文件：{check_yaml_path}")

    def change_check_version(self):
        """修改安装检查是否是最新版本"""
        check_path = os.path.join(self.check_dir, 'inst', f'Seeyon{self.product_line.upper()}Install_real.bat')
        if os.path.isfile(check_path):
            self.change_check_version_file(check_path)
        else:
            logger.info(f"没有找到修改检查是否最新版本的配置文件：{check_path}")

    def run_as_admin(self):
        params = (f'Start-Process "{self.install_workspace}\\{self.package_name.replace(".zip", "")}'
                  f'\\Seeyon{self.product_line}Install.bat" -Verb RunAs')
        cmd = f"powershell -Command {params}"
        call_command(cmd)

    @retry(tries=15, delay=2)
    def get_install_window(self):
        logger.info(f"开始等待获取安装程序窗口")
        try:
            self.get_cmd_window()
        except Exception as err:
            logger.error(repr(err))
        # 获取所有窗口
        titles = pygetwindow.getAllTitles()
        for title in titles:
            # if self.version in title and "安装程序" in title:
            if "安装程序" in title:
                logger.info("找到了InstallAnywhere安装窗口")
                time.sleep(15)  # 等待窗口加载完
                window = pygetwindow.getWindowsWithTitle(title)[0]
                return window

        logger.info("没有找到InstallAnywhere安装窗口，继续点击cmd启动窗口")
        raise RuntimeError('没有找到InstallAnywhere安装窗口')

    def welcome_accept(self, window):
        """选择欢迎-接受"""
        task = "选择欢迎-接受，等待点击下一步"
        position = (373, 319)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))
        self.agent_verify(window, task)

    def welcome_no_accept(self, window):
        """选择欢迎-不接受"""
        task = "选择欢迎-不接受"
        position = (373, 346)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))

    def password_info_input(self, window):
        # 初始化管理员账号
        position = (459, 103)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('init-admin', interval=0.1)

        position = (459, 135)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 167)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 223)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 255)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 287)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 319)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

    def copy_soft_dog(self):
        soft_dog_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                     'utils', 'partaletindev.js')
        remote_path = f"{self.install_path}\ApacheJetspeed\webapps\seeyon\common\js\\ui\partaletindev.js"
        shutil.copyfile(soft_dog_path, remote_path)


if __name__ == "__main__":
    tool = WindowsInstallTools()
    logger.info(tool.delete_registry_key())
