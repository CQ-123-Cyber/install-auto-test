import os
import shutil

from utils.file_tools import handle_remove_read_only
from dotenv import load_dotenv
from utils.time_help import datetime2str_by_format


class ConfLoad:
    def __init__(self):
        load_dotenv()
        self.ai_verify = os.getenv('ai_verify', '').lower() == 'true'
        self.has_verify_code = os.getenv('has_verify_code', 'false').lower() == 'true'
        self.package_name = os.getenv('package_name')
        if not self.package_name:
            raise Exception(f"没有找到环境变量：package_name")
        self.package_download_url = os.getenv('package_download_url')
        if not self.package_download_url:
            raise Exception(f"没有找到环境变量：package_download_url")
        self.product_line = os.getenv('product_line')
        if not self.product_line:
            raise Exception(f"没有找到环境变量：product_line")
        self.workspace = os.getenv('workspace')
        if not self.workspace:
            raise Exception(f"没有找到环境变量：workspace")
        if not os.path.isdir(self.workspace):
            os.makedirs(self.workspace)
        self.version = os.getenv('version')
        if not self.version:
            raise Exception(f"没有找到环境变量：version")
        self.install_path = os.getenv('install_path')
        if not self.install_path:
            raise Exception(f"没有找到环境变量：install_path")
        self.sql_type = os.getenv('sql_type')
        if not self.sql_type:
            raise Exception(f"没有找到环境变量：sql_type")

        self.verify_code = ''
        # 按天缓存验证码，验证码每天修改一次
        self.verify_code_cache_path = os.path.join(self.workspace,
                                                   f'verify_code_cache.{datetime2str_by_format(dt_format="%Y-%m-%d")}')
        # 安装包解压目录
        self.check_dir = f'{self.workspace}\\{self.package_name.replace(".zip", "")}'
        self.screenshots_dir = self.get_screenshots_dir()

    def delete_install_path(self):
        if os.path.isdir(self.install_path):
            shutil.rmtree(self.install_path, onerror=handle_remove_read_only)

    @staticmethod
    def get_screenshots_dir():
        screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'screenshots')
        if os.path.isdir(screenshots_dir):
            shutil.rmtree(screenshots_dir, onerror=handle_remove_read_only)
        if not os.path.isdir(screenshots_dir):
            os.makedirs(screenshots_dir)
        return screenshots_dir
