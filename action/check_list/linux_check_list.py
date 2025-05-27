import os
import pyautogui
from loguru import logger

from action.check_list.check_list import CheckList
from utils.ssh_tools import get_ssh_client


class LinuxCheckList(CheckList):
    """
    定义安装程序的检查项
    """

    def __init__(self, install_tool):
        super().__init__(install_tool)
        self.install_tool = install_tool
        self.ssh_tools = get_ssh_client()

    def check_install_dir(self):
        """
        检查安装包解压目录
        """
        check_dir_file_list = self.ssh_tools.list_remote_directory(self.check_dir)
        exist_file_list = ['data', 'inst', 'intl_SeeyonA8-1Install.bat', 'intl_SeeyonA8-1Install.sh',
                           'intl_SeeyonA8-2Install.bat', 'intl_SeeyonA8-2Install.sh', 'java', 'readme.txt',
                           'SeeyonA6-1Install.bat', 'SeeyonA6-1Install.sh', 'SeeyonA8-1Install.bat',
                           'SeeyonA8-1Install.sh', 'SeeyonA8-2Install.bat', 'SeeyonA8-2Install.sh',
                           'SeeyonA8TX-1Install.bat', 'SeeyonA8TX-1Install.sh', 'SeeyonA8TX-2Install.bat',
                           'SeeyonA8TX-2Install.sh', 'SeeyonG6-1Install.bat', 'SeeyonG6-1Install.sh',
                           'SeeyonG6-2Install.bat', 'SeeyonG6-2Install.sh', 'SeeyonG6NV5-1Install.bat',
                           'SeeyonG6NV5-1Install.sh', 'SeeyonG6NV5-2Install.bat', 'SeeyonG6NV5-2Install.sh',
                           'SeeyonG6SCV5-1Install.bat', 'SeeyonG6SCV5-1Install.sh', 'SeeyonG6SCV5-2Install.bat',
                           'SeeyonG6SCV5-2Install.sh', 'SeeyonG6SUV5-1Install.bat', 'SeeyonG6SUV5-1Install.sh',
                           'SeeyonG6SUV5-2Install.bat', 'SeeyonG6SUV5-2Install.sh', 'SeeyonN6-1Install.bat',
                           'SeeyonN6-1Install.sh', 'SeeyonN6-2Install.bat', 'SeeyonN6-2Install.sh',
                           'SeeyonS1AgentInstall.bat', 'SeeyonS1AgentInstall.sh', 'SeeyonS1AgentInstall_en.bat',
                           'SeeyonS1AgentInstall_en.sh', 'updateDog']
        for file_name in exist_file_list:
            if file_name not in check_dir_file_list:
                raise Exception(f"检查安装包解压目录失败，{file_name}不存在")

    def check_welcome_accept(self, window):
        """
        检查【欢迎】页面
        """
        task = "欢迎"
        screenshot = self.check_from_base(task, window)
        self.agent_check('当前"不接受"选项处于激活状态"', screenshot)
        # 验证上一步没激活
        self.install_tool.click_last_step(window, '欢迎', '欢迎')
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        self.agent_check('当前处于"欢迎-软件许可协议"界面', screenshot)
        # 验证上一步没激活
        self.install_tool.click_next_step(window, '欢迎', '欢迎', is_verify=False)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        self.agent_check('当前处于"欢迎-软件许可协议"界面', screenshot)

        self.install_tool.welcome_accept(window)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        self.agent_check('当前"接受"选项处于激活状态', screenshot)

        # linux转发的窗口对弹窗支持不友好，暂时不检查

    def check_registry_key(self):
        """
        安装完成后检查注册表
        """
        logger.info(f"安装完成，检查注册表是否注册成功")
        registry_file_path = '/root/.config/seeyon/fake_registry.info'
        if self.ssh_tools.remote_file_exists(registry_file_path):
            logger.info(f"注册表验证成功，{registry_file_path}存在")
            data = self.ssh_tools.read_remote_file(registry_file_path)
            for line in data.split():
                line = line.strip()
                if not line:
                    continue
                line_list = line.split('=')
                if len(line_list) < 2:
                    continue
                value_name = line_list[0].strip()
                value_data = line_list[1].strip()
                logger.info(f"Name = {value_name}, Data = {value_data}")
                if value_name == 'SEEYON_VERSION':
                    assert self.version.lower() in value_data.lower(), \
                        f"注册表中SEEYON_VERSION不正确：SEEYON_VERSION={value_data}, env.version={self.version}"
                if value_name == 'SEEYON_PATH':
                    assert os.path.normpath(value_data) == os.path.normpath(
                        self.install_path), f"注册表中SEEYON_PATH不正确：SEEYON_PATH={value_data}, env.install_path={self.install_path}"
                if value_name == 'SEEYON_EDITION':
                    product_line_list = self.product_line.split('-')
                    assert value_data == f"{product_line_list[0]}V5-{product_line_list[1]}", \
                        f"注册表中SEEYON_EDITION不正确：SEEYON_EDITION={value_data}, env.product_line={self.product_line}"
        else:
            logger.error(f"注册表验证失败，{registry_file_path}不存在")
            raise

    def check_finish_install_path(self):
        pass
