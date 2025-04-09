import os
import shutil

from conf.settings import NODES
from utils.file_tools import handle_remove_read_only
from conf.settings import package_download_url, ai_verify, has_verify_code


class ConfLoad:
    def __init__(self):
        self.ai_verify = ai_verify
        self.node = self.get_install_node()
        self.workspace = self.get_workspace()
        self.product_line = self.get_product_line()
        self.version = self.get_version()
        self.package_name, self.package_download_url = self.get_package_info()
        self.screenshots_dir = self.get_screenshots_dir()
        self.install_path = self.node['install_path']
        self.sql_type = self.node['sql_type']
        self.has_verify_code = has_verify_code
        self.verify_code = ''

    def delete_install_path(self):
        if os.path.isdir(self.install_path):
            shutil.rmtree(self.install_path, onerror=handle_remove_read_only)

    @staticmethod
    def get_install_node():
        """根据环境变量获取测试节点"""
        node_name = os.getenv('INSTALL_NODE', '')
        if not node_name in NODES.keys():
            raise RuntimeError(f"请在环境变量INSTALL_NODE设置安装节点名称")
        return NODES[node_name]

    def get_product_line(self):
        """测试的产品线，如：A8-2"""
        return self.node['product_line']

    def get_version(self):
        """测试的版本，如：V9.1"""
        return self.node['version']

    def get_workspace(self):
        workspace = self.node['workspace']
        if not os.path.isdir(workspace):
            os.makedirs(workspace)
        return workspace

    @staticmethod
    def get_package_info():
        package_name = package_download_url.split('/')[-1]
        return package_name, package_download_url

    @staticmethod
    def get_screenshots_dir():
        screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'screenshots')
        if not os.path.isdir(screenshots_dir):
            os.makedirs(screenshots_dir)
        return screenshots_dir
