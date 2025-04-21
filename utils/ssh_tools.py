import paramiko
from retry import retry

from loguru import logger


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

    def upload_file(self, local_path, remote_path):
        try:
            sftp = self.ssh.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            logger.info(f"文件 {local_path} 上传到 {remote_path} 成功")
        except Exception as e:
            raise RuntimeError(f"上传 {local_path} 到 {remote_path} 失败: {repr(e)}")

    def download_file(self, remote_path, local_path):
        try:
            sftp = self.ssh.open_sftp()
            sftp.get(remote_path, local_path)
            sftp.close()
            logger.info(f"文件 {remote_path} 下载到 {local_path} 成功")
        except Exception as e:
            raise RuntimeError(f"下载 {remote_path} 到 {local_path} 失败: {repr(e)}")

    def remote_file_exists(self, remote_path):
        try:
            sftp = self.ssh.open_sftp()
            try:
                sftp.stat(remote_path)
                file_exists = True
            except FileNotFoundError:
                file_exists = False
            sftp.close()
            return file_exists
        except Exception as e:
            raise RuntimeError(f"判断远程文件 {remote_path} 是否存在时出错: {repr(e)}")

    def list_remote_directory(self, remote_directory):
        try:
            sftp = self.ssh.open_sftp()
            item_list = sftp.listdir(remote_directory)
            sftp.close()
            return item_list
        except IOError as e:
            raise RuntimeError(f"Failed to list directory {remote_directory}: {repr(e)}")

    def read_remote_file(self, remote_file_path):
        try:
            sftp = self.ssh.open_sftp()
            with sftp.open(remote_file_path, 'r') as remote_file:
                file_contents = remote_file.read()
            sftp.close()
            return file_contents.decode('utf-8')
        except IOError as e:
            raise RuntimeError(f"Failed to read remote file {remote_file_path}: {repr(e)}")

    def __del__(self):
        if hasattr(self, "ssh") and hasattr(self.ssh, "close"):
            self.ssh.close()


def get_ssh_client():
    return SSHClient(ip='192.168.225.11', port=15051, password='seeyon@123..', username='root')
