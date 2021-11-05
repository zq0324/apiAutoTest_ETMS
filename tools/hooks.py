#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
@project: apiAutoTest
@file: hooks.py
@author: zy7y
@time: 2021/2/27
@site: https://cnblogs.com/zy7y
@github: https://github.com/zy7y
@gitee: https://gitee.com/zy7y
@desc: 扩展方法, 2021/02/27
关于exec执行python代码可查阅资料：https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p23_executing_code_with_local_side_effects.html

"""
import json
import time


def get_current_highest():
    """获取当前时间戳"""
    return int(time.time())


def sum_data(a, b):
    """计算函数"""
    return a + b


def set_token(token: str):
    """设置token，直接返回字典"""
    return {"Authorization": token}


def username():
    """生成随机用户名"""
    import random
    import string
    return "test_" + "".join(random.sample(string.ascii_letters + string.digits, 10))


def file_url(url):
    return '/'.join(url.split('/')[-4:])


if __name__ == '__main__':
    print(file_url('http://127.0.0.1:80/api/test/20211104/14/2e96da901a2949dab4cda66c96517069'))