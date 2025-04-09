import os
import re
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
from utils.ssh_tools import SSHClient


class LinuxInstallTools(InstallTools):
    def __init__(self):
        super().__init__()
        self.ssh_client = SSHClient(ip='192.168.225.11', port=15051, password='seeyon@123..', username='root')

    def delete_registry_key(self):
        # self.ssh_client.exec_command('ls')
        # if code != 0:
        #     raise Exception(f"删除注册信息失败")
        self.ssh_client.exec_command('cd /home/tenghc/0.SeeyonInstall && export DISPLAY=10.1.203.235:0.0;bash SeeyonA8-2Install.sh')



if __name__ == "__main__":
    tools = LinuxInstallTools()
    tools.delete_registry_key()
