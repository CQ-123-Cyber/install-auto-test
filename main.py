import os
import sys

from dotenv import load_dotenv
from loguru import logger

from action.linux_upgrade import LinuxUpgradeTools
from action.windows import WindowsInstallTools
# from action.linux import LinuxInstallTools
from utils.cmd_tools import getoutput
from action.database import get_database_cls, Database
from action import linux_upgrade


def create_tools(new_value=None):
    os_system = os.getenv('os_system', 'linux')
    logger.info(f"从环境变量识别到os_system={os_system}")
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env', os_system, '.env')
    if not os.path.isfile(dotenv_path):
        raise Exception(f".env文件不存在：{dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path)

    if os_system == 'windows':
        tools = WindowsInstallTools()
    elif os_system == 'linux':
        tools = LinuxUpgradeTools()
        # 如果提供了new_value参数，则设置到tools实例中
        if new_value:
            tools.new_value = new_value
    else:
        raise Exception(f"操作系统待实现：{os_system}")
    return tools


def create_database(begin_database_name='admin', sql_type='mysql'):
    logger.info(f'BUILD_USER={begin_database_name}')
    d = get_database_cls(sql_type, begin_database_name=begin_database_name)
    try:
        d.create_database()
    except Exception as e:
        if "database exists" in str(e):
            logger.info(f"数据库已存在，跳过创建")
        else:
            raise e
    data = d.get_input_data()
    data.update({'sql_type': sql_type})
    logger.info(f"创建的数据库信息：{data}")
    database_name = data['database_name']
    return database_name


def main():
    # 创建数据库并获取数据库名称
    # 删除重复调用，只保留一次create_database
    database_name = create_database()
    linux_upgrade.database_name = database_name
    logger.info(f"获取到的数据库名称: {database_name}")

    # 创建工具实例并传入数据库名称
    tools = create_tools(new_value=database_name)

    # 现在tools.new_value已经是database_name的值
    logger.info(f"设置的数据库名称: {tools.new_value}")

    # 执行修改文件操作c的
    tools.modify_file_with_sed()

    # 其他操作...
    # assert isinstance(tools, LinuxInstallTools)  # 开发调试用
    logger.info(f"开始验证码")
    tools.get_verify_code()
    #logger.info(f"开始删除安装目标目录")
    #tools.delete_registry_key()
    tools.delete_install_path()
    #tools.download()
    tools.unzip_package()
    tools.change_check_config()
    tools.change_check_version()

    process = None
    try:
        process = tools.run_as_admin()
        install_window = tools.get_install_window()
        tools.install_steps(install_window)
        tools.check_list.check_registry_key()
        tools.copy_soft_dog()
    finally:
        if process:
            process.terminate()
        getoutput('taskkill /IM Xmanager.exe /F')

    tools.check_list.check_finish_install_path()


if __name__ == "__main__":
    main()
