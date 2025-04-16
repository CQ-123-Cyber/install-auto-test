import os
import winreg
from loguru import logger

from action.check_list.check_list import CheckList


class WindowsCheckList(CheckList):
    """
    定义安装程序的检查项
    """

    def __init__(self, install_tool):
        super().__init__(install_tool)
        self.install_tool = install_tool

    def check_install_dir(self):
        """
        检查安装包解压目录
        """
        check_dir_file_list = os.listdir(self.check_dir)
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

    def check_registry_key(self):
        """
        安装完成后检查注册表
        """
        logger.info(f"安装完成，检查注册表是否注册成功")
        try:
            with (winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 'SOFTWARE\WOW6432Node\SEEYON\A8',
                                 0,
                                 winreg.KEY_READ) as key):
                i = 0
                while True:
                    try:
                        value_name, value_data, value_type = winreg.EnumValue(key, i)
                        logger.info(f"Value {i}: Name = {value_name}, Data = {value_data}, Type = {value_type}")
                        if value_name == 'SEEYON_VERSION':
                            assert value_data.lower() == self.version.lower(), f"注册表中SEEYON_VERSION不正确：SEEYON_VERSION={value_data}, env.version={self.version}"
                        if value_name == 'SEEYON_PATH':
                            assert os.path.normpath(value_data) == os.path.normpath(
                                self.install_path), f"注册表中SEEYON_PATH不正确：SEEYON_PATH={value_data}, env.install_path={self.install_path}"
                        if value_name == 'SEEYON_EDITION':
                            product_line_list = self.product_line.split('-')
                            assert value_data == f"{product_line_list[0]}V5-{product_line_list[1]}", f"注册表中SEEYON_EDITION不正确：SEEYON_EDITION={value_data}, env.product_line={self.product_line}"
                        i += 1
                    except OSError:
                        break
                logger.info(f"注册表验证成功，HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\SEEYON\A8存在")
        except FileNotFoundError:
            logger.error(f"注册表验证失败，HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\SEEYON不存在")
            raise

    def check_finish_install_path(self):
        """
        安装完成后检查安装目录
        """
        logger.info("开始安装完成后检查安装目录")
        check_dir_file_list = os.listdir(self.install_path)
        exist_file_list = ['ApacheJetspeed', 'base', 'inst', 'jdk', 'Logs', 'OfficeTrans',
                           'S1', 'seeyontools', 'Uninstall_A8', 'Uninstall_jdk']
        for file_name in exist_file_list:
            if file_name not in check_dir_file_list:
                raise Exception(f"检查安装包安装完成后目录文件列表失败，{file_name}不存在")
        logs_exist_file_list = ['all.log', 'err.log', 'STDERR_MSG.LOG', 'STDOUT_MSG.LOG']
        logs_dir = os.path.join(self.install_path, 'Logs')
        if not os.path.isdir(logs_dir):
            raise Exception(f"安装完成后，Log目录在安装目录下不存在：{logs_dir}")
        for file_name in logs_exist_file_list:
            if file_name not in os.listdir(logs_dir):
                raise Exception(f"检查安装包安装完成后目录文件列表失败，Logs/{file_name}不存在")
