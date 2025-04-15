import os

from action.check_list.check_list import CheckList


class LinuxCheckList(CheckList):
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
