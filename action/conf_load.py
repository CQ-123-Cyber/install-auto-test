import os
import shutil
from loguru import logger

from utils.file_tools import handle_remove_read_only
from utils.time_help import datetime2str_by_format
from utils.name_tools import verify_name


class ConfLoad:
    def __init__(self):
        self.ai_verify = os.getenv('ai_verify', '').lower() == 'true'
        self.has_verify_code = os.getenv('has_verify_code', 'false').lower() == 'true'
        self.is_check_list = os.getenv('is_check_list', '').lower() == 'true'
        self.job_name = os.getenv('job_name')
        if not self.job_name:
            raise Exception(f"没有找到环境变量：job_name")
        if not verify_name(self.job_name):
            raise Exception(f"job_name必须以自己的协同登录名开头，例如：tenghc_xxx")
        self.os_system = os.getenv('os_system')
        if not self.os_system:
            raise Exception(f"没有找到环境变量：os_system")
        self.package_download_url = os.getenv('package_download_url')
        if not self.package_download_url:
            raise Exception(f"没有找到环境变量：package_download_url")

        self.package_name = self.package_download_url.split('/')[-1]
        if not self.package_name:
            raise Exception(f"从package_download_url获取package_name失败")

        self.product_line = os.getenv('product_line')
        if not self.product_line:
            raise Exception(f"没有找到环境变量：product_line")
        self.install_workspace = os.getenv('install_workspace')
        if not self.install_workspace:
            raise Exception(f"没有找到环境变量：install_workspace")
        if not os.path.isdir(self.install_workspace):
            os.makedirs(self.install_workspace)
        self.version = os.getenv('version')
        if not self.version:
            raise Exception(f"没有找到环境变量：version")
        self.install_path = os.getenv('install_path')
        if not self.install_path:
            raise Exception(f"没有找到环境变量：install_path")
        self.install_path = self.install_path.format(self.job_name)
        self.sql_type = os.getenv('sql_type')
        if not self.sql_type:
            raise Exception(f"没有找到环境变量：sql_type")

        self.verify_code = ''
        # 按天缓存验证码，验证码每天修改一次
        self.verify_code_cache_path = f'verify_code_cache.{datetime2str_by_format(dt_format="%Y-%m-%d")}'
        # 安装包解压目录
        self.check_dir = f'{self.install_workspace}/{self.package_name.replace(".zip", "")}'
        self.screenshots_dir = self.reset_screenshots_dir()

        # 基准截图目录
        self.base_screenshots_dir = os.path.join(self.install_workspace, 'base_screenshots', self.version,
                                                 self.product_line, self.os_system)

    def reset_screenshots_dir(self):
        logger.info("开始重置截图目录")
        screenshots_dir = os.path.join(self.install_workspace, 'screenshots')
        if os.path.isdir(screenshots_dir):
            shutil.rmtree(screenshots_dir, onerror=handle_remove_read_only)
        if not os.path.isdir(screenshots_dir):
            os.makedirs(screenshots_dir)
        return screenshots_dir

    def print_var(self):
        var_list = ['package_download_url', 'package_name', 'product_line', 'version', 'install_workspace',
                    'install_path', 'sql_type', 'os_system', 'has_verify_code', 'ai_verify', 'is_check_list']
        for v in var_list:
            logger.info(f"{v}={getattr(self, v)}")
