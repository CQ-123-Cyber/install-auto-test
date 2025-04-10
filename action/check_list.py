import os
import pyautogui
from retry import retry

from agent.agent import Agent
from action.conf_load import ConfLoad
from utils.screenshot_tools import to_screenshot_b64, load_png_to_screenshot_b64


class CheckList(ConfLoad):
    """
    定义安装程序的检查项
    """

    def __init__(self, install_tool):
        super().__init__()
        self.install_tool = install_tool
        # 基准截图目录
        self.base_screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                 'base_screenshots', str(self.version), str(self.product_line))

    @retry(tries=3, delay=5)
    def agent_check_from_base(self, task, screenshot, base_screenshot):
        if self.ai_verify:
            content = Agent.check_from_base(task, to_screenshot_b64(screenshot), base_screenshot)
            if content:
                status = content['status']
                if status == "不正确":
                    raise RuntimeError(f"使用AI检查页面不正确：\n{content}")

    @retry(tries=3, delay=1)
    def agent_check(self, task, screenshot):
        if self.ai_verify:
            content = Agent.check(task, to_screenshot_b64(screenshot))
            if content:
                status = content['status']
                if status == "不正确":
                    raise RuntimeError(f"使用AI检查页面不正确：\n{content}")

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

    def check_from_base(self, task, window):
        if not os.path.isdir(self.base_screenshots_dir):
            os.makedirs(self.base_screenshots_dir)
        base_screenshot_path = os.path.join(self.base_screenshots_dir, f'{task}.png')
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        if not os.path.isfile(base_screenshot_path):
            screenshot.save(base_screenshot_path)
        base_screenshot = load_png_to_screenshot_b64(base_screenshot_path)
        self.agent_check_from_base(task, screenshot, base_screenshot)
        return screenshot

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

        self.install_tool.welcome_no_accept(window)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        self.agent_check('出现警告，警告内容：如果不接受许可协议条款，那么不能继续安装', screenshot)
        self.install_tool.welcome_no_accept_warn_continue(window)

    def check_install_path(self, window):
        """
        检查【安装路径】页面
        """
        task = "安装路径"
        self.check_from_base(task, window)

        self.install_tool.click_last_step(window, "安装路径", "欢迎")
        self.install_tool.click_next_step(window, "欢迎", "安装路径")
        self.install_tool.install_path_clean(window)
        self.install_tool.install_path_recover(window)
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        self.agent_check('当前安装路径输入框中有值', screenshot)

    def check_database(self, window):
        """
        检查【数据库】页面
        """
        task = "数据库"
        self.check_from_base(task, window)

        self.install_tool.click_last_step(window, "数据库", "安装路径")
        self.install_tool.click_next_step(window, "安装路径", "数据库")

    def check_password_info_input(self, window):
        """
        检查【账号密码设置】页面
        """
        task = "安装-账号密码设置"
        self.check_from_base(task, window)

        self.install_tool.click_last_step(window, "安装", "确认")
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        self.agent_check('当前处于安装-账号密码设置界面', screenshot)
