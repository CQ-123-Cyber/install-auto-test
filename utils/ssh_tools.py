import paramiko
from retry import retry


class SSHClient():
    def __init__(self, ip=None, host=None, port=None, username=None, user=None, password=None, **kwargs):
        self.host = ip or host
        self.port = port or 15001
        self.username = username or user or "root"
        self.password = password
        self.ssh = self.connect()
        self.channel = None

    @retry(tries=3, delay=3)
    def connect(self):
        ssh = paramiko.SSHClient()
        know_host = paramiko.AutoAddPolicy()
        ssh.set_missing_host_key_policy(know_host)
        try:
            ssh.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)
            return ssh
        except Exception as err:
            ssh.close()
            raise RuntimeError(f"{self.host}ssh连接失败: {repr(err)}")

    def exec_command(self, cmd):
        try:
            self.channel = self.ssh.get_transport().open_session()
            self.channel.exec_command(cmd)
            self.channel.shutdown_write()
            stdout_str = self.channel.makefile().read().decode()
            stderr_str = self.channel.makefile_stderr().read().decode()
            exit_code = self.channel.recv_exit_status()
            return exit_code, stdout_str + "\n" + stderr_str
        finally:
            if hasattr(self, "channel") and hasattr(self.channel, "close"):
                self.channel.close()

    def __del__(self):
        if hasattr(self, "ssh") and hasattr(self.ssh, "close"):
            self.ssh.close()
