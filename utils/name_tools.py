def verify_name(name: str):
    name_list = ['zhoul', 'zhaoxr', 'liudx', 'tangqi', 'tenghc', 'chenyao', 'xiaoym', 'yfei', 'duhl', 'shenym',
                 'xionghui', 'wangtao', 'admin', 'install', 'Seeyon']
    for sub_name in name_list:
        if name.startswith(sub_name):
            return True
    return False
