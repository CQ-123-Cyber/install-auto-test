import os
import re
import time
import subprocess
import pygetwindow
import winreg
import pyautogui
from retry import retry
from loguru import logger

from action.base import InstallTools
from utils.cmd_tools import call_command
from agent.agent import Agent
from utils.screenshot_tools import to_screenshot_b64
from utils.ssh_tools import SSHClient
from action.check_list.linux_check_list import LinuxCheckList
from action.check_list.no_check_list import NoCheckList


class LinuxInstallTools(InstallTools):
    def __init__(self):
        super().__init__()
        self.check_list = LinuxCheckList(self) if self.is_check_list == True else NoCheckList(self)
        self.ssh_client = SSHClient(ip='192.168.225.11', port=15051, password='seeyon@123..', username='root')
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
        pass

    def download(self):
        """下载安装程序"""
        cmd = f"curl {self.package_download_url} -o {self.install_workspace}/{self.package_name}"
        self.exec_cmd(cmd)

    def unzip_package(self):
        cmd = f"cd {self.install_workspace} && unzip {self.package_name}"
        self.exec_cmd(cmd)

if __name__ == "__main__":
    tools = LinuxInstallTools()
    tools.delete_registry_key()
