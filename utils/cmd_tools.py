import os
import copy
import subprocess


def console_to_str(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('gbk')


def call_command(cmd, cwd=None, env=None, shell=True):
    print("cmd:", str(cmd))
    new_env = env
    if env and isinstance(env, dict):
        now_env = copy.deepcopy(os.environ.copy())
        now_env.update(env)
        new_env = now_env
    ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell, cwd=cwd, env=new_env)
    for i in iter(ex.stdout.readline, b''):
        print(console_to_str(i).strip())
    if ex.wait() != 0:
        for i in iter(ex.stdout.readline, b''):
            print(console_to_str(i).strip())
        raise RuntimeError("cmd命令执行失败")


def call_command_get_out(cmd, cwd=None, env=None, shell=True):
    out = subprocess.check_output(cmd, cwd=cwd, env=env, shell=shell)
    out_lines = console_to_str(out).strip().split()
    return out_lines
