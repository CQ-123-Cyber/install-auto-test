import os
import re
import yaml
import time
from retry import retry
import pyautogui
import pygetwindow
from loguru import logger
from abc import abstractmethod

from action.conf_load import ConfLoad
from utils.cmd_tools import call_command
from agent.agent import Agent
from utils.screenshot_tools import to_screenshot_b64
from action.database import get_database_cls
from utils.time_help import datetime2str_by_format
from utils.language_tools import switch_input_method


class InstallTools(ConfLoad):
    def __init__(self):
        super().__init__()
        self.check_list = None
        self.print_var()

    def download(self):
        """下载安装程序"""
        cmd = f"curl {self.package_download_url} -o {self.install_workspace}/{self.package_name}"
        call_command(cmd)

    @retry(tries=3, delay=1)
    def get_verify_code_window(self):
        # 获取所有窗口
        titles = pygetwindow.getAllTitles()
        for title in titles:
            if "verify-code.exe" in title:
                logger.info(f"找到了验证码窗口：{title}")
                time.sleep(3)  # 等待窗口加载完
                window = pygetwindow.getWindowsWithTitle(title)[0]
                window.restore()
                window.activate()
                return window
        raise RuntimeError('没有找到cmd启动窗口')

    def load_verify_code(self):
        if os.path.isfile(self.verify_code_cache_path):
            logger.info(f"识别到存在验证码缓存文件，从缓存加载验证码")
            with open(self.verify_code_cache_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return None

    def write_verify_code(self):
        with open(self.verify_code_cache_path, 'w', encoding='utf-8') as f:
            f.write(self.verify_code)

    @retry(tries=5, delay=1)
    def get_verify_code(self):
        verify_code = self.load_verify_code()
        if verify_code:
            self.verify_code = verify_code
            logger.info(f"验证码：{self.verify_code}")
            return
        logger.info(f"验证码缓存文件不存在，开始运行验证码工具")
        self.run_verify_code()
        time.sleep(5)
        window = self.get_verify_code_window()
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'验证码.png'))
        window.close()
        verify_code_text = Agent.verify_code("识别出验证码", to_screenshot_b64(screenshot))
        pattern = r'\d{5}'
        matches = re.findall(pattern, verify_code_text)
        logger.info(f"正则匹配验证码结果：{matches}")
        if matches:
            self.verify_code = matches[0]
            logger.info(f"验证码：{self.verify_code}")
            self.write_verify_code()
            return
        raise Exception(f"AI获取验证码失败")

    @abstractmethod
    def delete_install_path(self):
        """删除安装目标目录"""

    @staticmethod
    @abstractmethod
    def delete_registry_key():
        """删除注册表"""

    @abstractmethod
    def unzip_package(self):
        """解压安装包"""

    @abstractmethod
    def run_as_admin(self):
        """使用管理员运行安装程序"""

    @abstractmethod
    def change_check_config(self):
        """修改安装检查项"""

    @staticmethod
    def change_check_config_file(config_file_path):
        """修改安装检查项"""
        with open(config_file_path, 'r') as file:
            data = yaml.safe_load(file)
        data['server']['vm']['warningMemoryMb'] = 0
        with open(config_file_path, 'w') as file:
            yaml.safe_dump(data, file)

    @abstractmethod
    def change_check_version(self):
        """修改安装检查是否是最新版本"""

    @staticmethod
    def change_check_version_file(version_file_path):
        """修改安装检查是否是最新版本"""
        today_date = datetime2str_by_format(dt_format='%Y-%m-%d')
        with open(version_file_path, 'r') as file:
            lines = file.readlines()

        # 修改日期
        updated_lines = []
        for line in lines:
            if '-Dseeyon_ctp_install_check_date=' in line:
                # 使用正则表达式来替换日期
                line = line.split('-Dseeyon_ctp_install_check_date=')[
                           0] + f'-Dseeyon_ctp_install_check_date={today_date} ' + \
                       line.split('-Dseeyon_ctp_install_check_date=')[1].split(' ')[1]
            updated_lines.append(line)

        # 写入修改后的内容到一个新的批处理文件
        with open(version_file_path, 'w') as file:
            file.writelines(updated_lines)

    @staticmethod
    def run_verify_code():
        verify_code_exe = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                       'tools', 'verify-code.exe')
        params = f'Start-Process "{verify_code_exe}"'
        cmd = f"powershell -Command {params}"
        call_command(cmd)

    @retry(tries=3, delay=5)
    def agent_verify(self, window, task):
        if self.ai_verify:
            screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
            screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))
            content = Agent.verify(task, to_screenshot_b64(screenshot))
            if content:
                status = content['status']
                if status == "不正确":
                    raise RuntimeError(f"使用AI验证操作结果不正确：\n{content}")

    @staticmethod
    # @retry(tries=12, delay=10)
    def get_cmd_window():
        # 获取所有窗口
        titles = pygetwindow.getAllTitles()
        find = False
        for title in titles:
            # jenkins的agent窗口忽略
            if "agent.jar" in title.lower().strip():
                continue
            if title.lower().strip() == "C:\WINDOWS\system32\cmd.exe".lower():
                logger.info("找到了cmd启动窗口")
                find = True
                window = pygetwindow.getWindowsWithTitle(title)[0]
                window.restore()
                # window.activate()
                time.sleep(3)
                logger.info(f"找到了cmd启动窗口，开始点击确认")
                pyautogui.moveTo(window.left + 10, window.top + 10)  # 将鼠标移动到窗口内
                pyautogui.click()  # 执行物理点击确保焦点
                pyautogui.hotkey('enter')  # 比单独press更可靠
        if not find:
            raise RuntimeError('没有找到cmd启动窗口')

    @abstractmethod
    def get_install_window(self):
        pass

    @staticmethod
    def change_language():
        screenshot = pyautogui.screenshot()
        language = Agent.language("输入法是中文还是英文", to_screenshot_b64(screenshot))
        if language == "中文":
            logger.info("切换输入法到英文")
            # pyautogui.hotkey('shift')
            switch_input_method()
            time.sleep(1)

    def install_steps(self, window):
        window.restore()
        window.activate()
        time.sleep(5)
        logger.info(f"安装窗口位置：{window.left}, {window.top}, {window.width}, {window.height}")

        self.check_list.check_install_dir()
        self.change_language()
        self.check_list.check_welcome_accept(window)
        self.welcome_accept(window)
        self.click_next_step(window, "欢迎", "安装路径")

        self.check_list.check_install_path(window)
        self.install_path_clean(window)
        self.install_path_input(window)
        self.click_next_step(window, "安装路径", "数据库")

        self.check_list.check_database(window)
        self.database_input(window)
        self.click_next_step(window, "数据库", "数据库")
        self.click_next_step(window, "数据库", "确认")
        self.click_next_step(window, "确认", "确认")
        self.click_next_step(window, "确认", "安装")
        time.sleep(60 * 4)  # 等待安装
        self.install_finish(window)

        self.check_list.check_password_info_input(window)
        self.password_info_input(window)
        self.click_next_step(window, "安装", "安装-IP访问控制")
        self.click_next_step(window, "安装", "安装完成，并且安装成功")
        self.click_next_step(window, "完成", "", is_verify=False, is_save=False)

    @staticmethod
    def help(window):
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        Agent.help("修改安装路径", to_screenshot_b64(screenshot))

    @staticmethod
    def scale_up_and_down(position, width, height):
        """按比例缩放，重新计算位置"""
        base_width = 616
        base_height = 439
        # 计算缩放比例
        scale_x = width / base_width
        scale_y = height / base_height
        # 按比例缩放位置
        new_x = int(position[0] * scale_x)
        new_y = int(position[1] * scale_y)
        new_position = (new_x, new_y)
        return new_position

    @abstractmethod
    def welcome_accept(self, window):
        """选择欢迎-接受"""
        pass

    @abstractmethod
    def welcome_no_accept(self, window):
        """选择欢迎-不接受"""
        pass

    def welcome_no_accept_warn_continue(self, window):
        """选择欢迎-不接受-警告-继续执行"""
        task = "选择欢迎-不接受-警告-继续执行"
        position = (450, 221)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))

    def click_next_step(self, window, frame_name, next_frame_name, is_verify=True, is_save=True):
        """点击下一步"""
        task = f"点击{frame_name}-下一步，进入{next_frame_name}"
        position = (549, 407)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        screenshot = None
        time.sleep(3)
        if is_save:
            screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
            screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))
        if is_verify and screenshot:
            self.agent_verify(window, task)

    def click_last_step(self, window, frame_name, next_frame_name):
        """点击上一步"""
        task = f"点击{frame_name}-上一步，进入{next_frame_name}"
        position = (459, 407)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        time.sleep(3)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))

    def install_path_clean(self, window):
        """清除安装路径"""
        task = "清除安装路径"
        position = (289, 217)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        time.sleep(1)

    def install_path_recover(self, window):
        """恢复安装路径"""
        task = "恢复安装路径"
        position = (435, 246)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        time.sleep(1)

    def install_path_input(self, window):
        task = "设置安装路径-input"
        pyautogui.write(self.install_path, interval=0.1)
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))
        self.agent_verify(window, task)

    def database_input(self, window):
        task = "设置数据库-input"
        sql_cls = get_database_cls(self.sql_type)
        sql_cls.create_database()

        # 设置host
        if self.has_verify_code:
            position = (321, 133)
        else:
            position = (321, 146)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(sql_cls.host, interval=0.1)

        # 设置端口
        if self.has_verify_code:
            position = (345, 159)
        else:
            position = (321, 174)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(sql_cls.port, interval=0.1)

        # 设置数据库名称
        if self.has_verify_code:
            position = (321, 187)
        else:
            position = (321, 200)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(sql_cls.database_name, interval=0.1)

        # 设置用户名
        if self.has_verify_code:
            position = (321, 211)
        else:
            position = (321, 226)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(sql_cls.user, interval=0.1)

        # 设置密码
        if self.has_verify_code:
            position = (321, 237)
        else:
            position = (321, 252)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(sql_cls.password, interval=0.1)

        # 验证码
        if self.has_verify_code:
            position = (321, 300)
            position = self.scale_up_and_down(position, window.width, window.height)
            pyautogui.click(window.left + position[0], window.top + position[1])
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(self.verify_code, interval=0.1)

        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))
        self.agent_verify(window, task)

    @retry(tries=15, delay=60)
    def install_finish(self, window):
        task = f"点击安装，进入安装界面，当前界面出现设置账号密码的输入框"
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))
        content = Agent.verify(task, to_screenshot_b64(screenshot))
        if content:
            status = content['status']
            if status == "不正确":
                raise RuntimeError(f"使用AI验证操作结果不正确：\n{content}")

    @abstractmethod
    def password_info_input(self, window):
        # 初始化管理员账号
        pass
