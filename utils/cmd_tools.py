import os
import socket
import copy
import subprocess
from loguru import logger


def console_to_str(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('gbk')


def call_command(cmd, cwd=None, env=None, shell=True):
    logger.info("cmd:" + str(cmd))
    new_env = env
    if env and isinstance(env, dict):
        now_env = copy.deepcopy(os.environ.copy())
        now_env.update(env)
        new_env = now_env
    ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell, cwd=cwd, env=new_env)
    for i in iter(ex.stdout.readline, b''):
        logger.info(console_to_str(i).strip())
    if ex.wait() != 0:
        for i in iter(ex.stdout.readline, b''):
            logger.info(console_to_str(i).strip())
        raise RuntimeError("cmd命令执行失败")


def call_command_get_out(cmd, cwd=None, env=None, shell=True):
    out = subprocess.check_output(cmd, cwd=cwd, env=env, shell=shell)
    out_lines = console_to_str(out).strip().split()
    return out_lines


def get_local_ip():
    s = None
    try:
        # 这里的 IP 地址和端口号是虚构的，只用来创建一个 UDP 连接以获取本机 IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        # 远端的地址不需要真实存在，只是为了触发获取本地IP的流程
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        if s:
            s.close()
    return ip


if __name__ == "__main__":
    print(get_local_ip())
