def verify_name(name: str):
    name_list = ['zhoul', 'zhaoxr', 'liudx', 'tangqi', 'tenghc', 'chenyao', 'xiaoym', 'yfei', 'duhl', 'shenym',
                 'xionghui', 'wangtao', 'admin', 'install']
    for sub_name in name_list:
        if name.startswith(sub_name):
            return True
    return False
