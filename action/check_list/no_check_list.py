from action.conf_load import ConfLoad



class NoCheckList(ConfLoad):
    """
    定义安装程序的检查项
    """

    def __init__(self, install_tool):
        super().__init__()
        self.install_tool = install_tool

    def check_install_dir(self):
        pass

    def agent_check_from_base(self, task, screenshot, base_screenshot):
        pass

    def agent_check(self, task, screenshot):
        pass

    def check_from_base(self, task, window):
        pass

    def check_welcome_accept(self, window):
        pass

    def check_install_path(self, window):
        pass

    def check_database(self, window):
        pass

    def check_password_info_input(self, window):
        pass

    def check_registry_key(self):
        pass

    def check_finish_install_path(self):
        pass