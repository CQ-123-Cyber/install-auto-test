import os
import yaml
import time
import subprocess
import pygetwindow
import winreg
import pyautogui
from retry import retry
from loguru import logger
import multiprocessing

from action.base import InstallTools
from utils.cmd_tools import get_local_ip, getoutput
from utils.ssh_tools import get_ssh_client
from action.check_list.linux_check_list import LinuxCheckList
from action.check_list.no_check_list import NoCheckList


def run_as_admin_with_multiprocessing(check_dir, product_line):
    local_ip = get_local_ip()
    logger.info(f'获取到本机ip：{local_ip}')
    ssh_client = get_ssh_client()
    code, msg = ssh_client.exec_command(
        f'cd {check_dir} && export DISPLAY={local_ip}:0.0;bash Seeyon{product_line}Install.sh')
    logger.info(msg)


class LinuxInstallTools(InstallTools):
    def __init__(self):
        super().__init__()
        self.check_list = LinuxCheckList(self) if self.is_check_list == True else NoCheckList(self)
        self.ssh_client = get_ssh_client()
        self.exec_cmd(f'mkdir -p {self.install_workspace}')

    def exec_cmd(self, cmd):
        logger.info(cmd)
        code, msg = self.ssh_client.exec_command(cmd)
        if msg.strip():
            logger.info(msg)
        if code != 0:
            raise Exception(f"远程执行命令失败")

    def delete_install_path(self):
        assert self.install_path != '' and self.install_path != '/'
        logger.info(f"安装目标目录：{self.install_path}")
        cmd = f'rm -rf {self.install_path}'
        self.exec_cmd(cmd)

    def delete_registry_key(self):
        cmd = f'rm -rf /root/.config/seeyoninstall*'
        self.exec_cmd(cmd)

    def download(self):
        """下载安装程序"""
        cmd = f"curl {self.package_download_url} -o {self.install_workspace}/{self.package_name}"
        self.exec_cmd(cmd)

    def unzip_package(self):
        dest_dir = self.check_dir
        assert dest_dir != '' and dest_dir != '/'
        cmd = f"rm -rf {dest_dir}"
        self.exec_cmd(cmd)
        cmd = f"cd {self.install_workspace} && unzip {self.package_name}"
        self.exec_cmd(cmd)

    def change_check_config(self):
        """修改安装检查项"""
        check_yaml_path = os.path.join(self.check_dir, 'inst', 'check.yml').replace('\\', '/')
        local_yaml_path = "check.yml"
        if self.ssh_client.remote_file_exists(check_yaml_path):
            self.ssh_client.download_file(check_yaml_path, local_yaml_path)
            self.change_check_config_file(local_yaml_path)
            self.ssh_client.upload_file(local_yaml_path, check_yaml_path)
            print("修改完成，warningMemoryMb 已更改为 0")
        else:
            logger.info(f"没有找到修改安装检查项的配置文件：{check_yaml_path}")

    def change_check_version(self):
        """修改安装检查是否是最新版本"""
        check_path = os.path.join(self.check_dir, 'inst',
                                  f'Seeyon{self.product_line.upper()}Install_real.bat').replace('\\', '/')
        local_check_path = f'Seeyon{self.product_line.upper()}Install_real.bat'
        if self.ssh_client.remote_file_exists(check_path):
            self.ssh_client.download_file(check_path, local_check_path)
            self.change_check_version_file(local_check_path)
            self.ssh_client.upload_file(local_check_path, check_path)
        else:
            logger.info(f"没有找到修改检查是否最新版本的配置文件：{check_path}")

    def run_as_admin(self):
        """使用多进程运行安装程序"""
        getoutput('taskkill /IM Xmanager.exe /F')
        xmanager_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools',
                                     'xmanager.xdts')
        subprocess.Popen(xmanager_path, shell=True)
        logger.info("xmanager.xdts启动成功")
        process = multiprocessing.Process(target=run_as_admin_with_multiprocessing,
                                          args=(self.check_dir, self.product_line,))
        process.start()
        return process

    @retry(tries=15, delay=2)
    def get_install_window(self):
        logger.info(f"开始等待获取安装程序窗口")
        # 获取所有窗口
        titles = pygetwindow.getAllTitles()
        for title in titles:
            # if self.version in title and "安装程序" in title:
            if "安装程序" in title:
                logger.info("找到了InstallAnywhere安装窗口")
                time.sleep(10)  # 等待窗口加载完
                window = self.get_windows_use_title(title)
                return window

        logger.info("没有找到InstallAnywhere安装窗口，继续点击cmd启动窗口")
        screenshot = pyautogui.screenshot()
        screenshot.save(os.path.join(self.screenshots_dir, 'cur_agent_check.png'))
        raise RuntimeError('没有找到InstallAnywhere安装窗口')

    def welcome_accept(self, window):
        """选择欢迎-接受"""
        task = "选择欢迎-接受，等待点击下一步"
        position = (229, 319)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))
        self.agent_verify(window, task)

    def welcome_no_accept(self, window):
        """选择欢迎-不接受"""
        task = "选择欢迎-不接受"
        position = (229, 346)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))

    def password_info_input(self, window):
        # 初始化管理员账号
        position = (459, 93)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('init-admin', interval=0.1)

        position = (459, 124)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 153)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 209)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 237)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 267)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 295)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

    def copy_soft_dog(self):
        soft_dog_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                     'utils', 'partaletindev.js')
        remote_path = f"{self.install_path}/ApacheJetspeed/webapps/seeyon/common/js/ui/partaletindev.js"
        self.ssh_client.upload_file(soft_dog_path, remote_path)


if __name__ == "__main__":
    tools = LinuxInstallTools()
    tools.delete_registry_key()
