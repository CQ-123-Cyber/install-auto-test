import os
import sys
from dotenv import load_dotenv
from loguru import logger
import subprocess

from action.windows import WindowsInstallTools
from action.linux import LinuxInstallTools


def main():
    os_system = os.getenv('os_system', 'linux')
    logger.info(f"从环境变量识别到os_system={os_system}")
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env', os_system, '.env')
    if not os.path.isfile(dotenv_path):
        raise Exception(f".env文件不存在：{dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path)

    if os_system == 'windows':
        tools = WindowsInstallTools()
    elif os_system == 'linux':
        tools = LinuxInstallTools()
    else:
        raise Exception(f"操作系统待实现：{os_system}")

    if len(sys.argv) > 1 and sys.argv[1] == 'check_finish_install_path':
        tools.check_list.check_finish_install_path()
        return

    assert isinstance(tools, LinuxInstallTools)  # 开发调试用
    logger.info(f"开始验证码")
    tools.get_verify_code()
    logger.info(f"开始删除安装目标目录")
    tools.delete_install_path()
    tools.delete_registry_key()
    # tools.download()
    # tools.unzip_package()
    tools.change_check_config()
    tools.change_check_version()

    process = None
    try:
        process = tools.run_as_admin()
        install_window = tools.get_install_window()
        tools.install_steps(install_window)
        tools.check_list.check_registry_key()
    finally:
        if process:
            process.terminate()
        subprocess.call('taskkill /IM Xmanager.exe /F', shell=True)


if __name__ == "__main__":
    main()
