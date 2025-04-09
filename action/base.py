import os
import yaml
import time
from retry import retry
import pyautogui
from abc import abstractmethod

from action.conf_load import ConfLoad
from utils.cmd_tools import call_command
from agent.agent import Agent
from utils.screenshot_tools import to_screenshot_b64
from action.database import get_database_cls
from action.check_list import CheckList


class InstallTools(ConfLoad):
    def download(self):
        """下载安装程序"""
        cmd = f"curl {self.package_download_url} -o {self.workspace}/{self.package_name}"
        call_command(cmd)

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
    def get_verify_code(self):
        """获取验证码"""

    def change_check_config(self):
        """修改安装检查项"""
        check_yaml_path = os.path.join(self.check_dir, 'inst', 'check.yml')
        with open(check_yaml_path, 'r') as file:
            data = yaml.safe_load(file)
        data['server']['vm']['warningMemoryMb'] = 0
        with open(check_yaml_path, 'w') as file:
            yaml.safe_dump(data, file)
        print("修改完成，warningMemoryMb 已更改为 0")

    @staticmethod
    def run_verify_code():
        verify_code_exe = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                       'tools', 'verify-code.exe')
        params = f'Start-Process "{verify_code_exe}" -Verb RunAs'
        cmd = f"powershell -Command {params}"
        call_command(cmd)

    @retry(tries=3, delay=5)
    def agent_verify(self, task, screenshot):
        if self.ai_verify:
            content = Agent.verify(task, to_screenshot_b64(screenshot))
            if content:
                status = content['status']
                if status == "不正确":
                    raise RuntimeError(f"使用AI验证操作结果不正确：\n{content}")

    @staticmethod
    def change_language():
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot.png')
        language = Agent.language("输入法是中文还是英文", to_screenshot_b64(screenshot))
        if language == "中文":
            print("切换输入法到英文")
            pyautogui.hotkey('shift')
            time.sleep(1)

    def install_steps(self, window):
        window.restore()
        window.activate()
        time.sleep(5)
        print(window.left, window.top, window.width, window.height)

        check_list = CheckList(self)
        check_list.check_install_dir()
        self.change_language()
        check_list.check_welcome_accept(window)
        self.welcome_accept(window)
        self.click_next_step(window, "欢迎", "安装路径")

        check_list.check_install_path(window)
        self.install_path_clean(window)
        self.install_path_input(window)
        self.click_next_step(window, "安装路径", "数据库")

        check_list.check_database(window)
        self.database_input(window)
        self.click_next_step(window, "数据库", "数据库")
        self.click_next_step(window, "数据库", "确认")
        self.click_next_step(window, "确认", "确认")
        self.click_next_step(window, "确认", "安装")
        self.install_finish(window)

        check_list.check_password_info_input(window)
        self.password_info_input(window)
        self.click_next_step(window, "安装", "安装-IP访问控制")
        self.click_next_step(window, "安装", "安装完成，并且安装成功")
        self.click_next_step(window, "完成", "", is_verify=False)

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

    def welcome_accept(self, window):
        """选择欢迎-接受"""
        task = "选择欢迎-接受，等待点击下一步"
        position = (373, 319)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))
        self.agent_verify(task, screenshot)

    def welcome_no_accept(self, window):
        """选择欢迎-不接受"""
        task = "选择欢迎-不接受"
        position = (373, 346)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))

    def welcome_no_accept_warn_continue(self, window):
        """选择欢迎-不接受-警告-继续执行"""
        task = "选择欢迎-不接受-警告-继续执行"
        position = (450, 221)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))

    def click_next_step(self, window, frame_name, next_frame_name, is_verify=True):
        """点击下一步"""
        task = f"点击{frame_name}-下一步，进入{next_frame_name}"
        position = (549, 407)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        time.sleep(3)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))
        if is_verify:
            self.agent_verify(task, screenshot)

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
        pyautogui.typewrite(self.install_path, interval=0.1)
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))
        self.agent_verify(task, screenshot)

    def database_input(self, window):
        task = "设置数据库-input"
        sql_cls = get_database_cls(self.sql_type)
        sql_cls.create_database()

        # 设置host
        position = (321, 133)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.write(sql_cls.host, interval=0.1)

        # 设置端口
        position = (345, 159)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(sql_cls.port, interval=0.1)

        # 设置数据库名称
        position = (321, 187)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.write(sql_cls.database_name, interval=0.1)

        # 设置用户名
        position = (321, 211)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.write(sql_cls.user, interval=0.1)

        # 设置密码
        position = (321, 237)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.write(sql_cls.password, interval=0.1)

        # 验证码
        position = (321, 300)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.write(self.verify_code, interval=0.1)

        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))
        self.agent_verify(task, screenshot)

    @retry(tries=20, delay=60)
    def install_finish(self, window):
        task = f"点击安装，进入安装界面，等待设置账号密码"
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(os.path.join(self.screenshots_dir, f'{task}.png'))
        # time.sleep(60*7)
        content = Agent.verify(task, to_screenshot_b64(screenshot))
        if content:
            status = content['status']
            if status == "不正确":
                raise RuntimeError(f"使用AI验证操作结果不正确：\n{content}")

    def password_info_input(self, window):
        # 初始化管理员账号
        position = (459, 103)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('init-admin', interval=0.1)

        position = (459, 135)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 167)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 223)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 255)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 287)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)

        position = (459, 319)
        position = self.scale_up_and_down(position, window.width, window.height)
        pyautogui.click(window.left + position[0], window.top + position[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('Ab123456', interval=0.1)
