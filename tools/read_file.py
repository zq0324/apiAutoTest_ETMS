#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: read_file.py
@ide: PyCharm
@time: 2020/7/31
@desc： 更新时间 2020/11/21 15：34 后续所有关于文件读取的方法全部收纳与此
"""
import os
import yaml
import xlrd
from tools import extractor


class ReadFile:
    config_dict = None
    case_file_list = []

    @classmethod
    def get_config_dict(cls, config_path: str = 'config/config.yaml') -> dict:
        """读取配置文件，并且转换成字典
        :param config_path: 配置文件地址， 默认使用当前项目目录下的config/config.yaml
        return cls.config_dict
        """
        if cls.config_dict is None:
            # 指定编码格式解决，win下跑代码抛出错误
            with open(config_path, 'r', encoding='utf-8') as file:
                cls.config_dict = yaml.load(
                    file.read(), Loader=yaml.FullLoader)
        return cls.config_dict

    @classmethod
    def read_config(cls, expr: str = '.'):
        """默认读取config目录下的config.yaml配置文件，根据传递的expr jsonpath表达式可任意返回任何配置项
        :param expr: 提取表达式, 使用jsonpath语法,默认值提取整个读取的对象
        return 根据表达式返回的值
        """
        return extractor(cls.get_config_dict(), expr)

    @classmethod
    def read_case_yml(cls, tag=None):
        """
        读取yml格式用例
        :tag： 用例tag，根据入参参数返回用例
        """
        cls.get_file(cls.read_config('$.file_path.test_case'))
        print(cls.case_file_list)
        for file in cls.case_file_list:
            with open(file, 'r', encoding='utf-8') as f:
                case_list = yaml.load(
                    f.read(), Loader=yaml.FullLoader)
            for case_tmp in case_list:
                case_tag = case_tmp.get('tag') if case_tmp.get('tag') else []
                if case_tmp.get('enable'):
                    if tag:
                        if tag in case_tag:
                            yield case_tmp
                    else:
                        yield case_tmp

    @classmethod
    def get_file(cls, file_path):
        """
        读取目录下所有yml，yaml格式用例数据
        :file_path:  用例的目录地址
        """
        file_list = os.listdir(file_path)
        file_list.sort(key=str.lower)
        for file in file_list:
            file = os.path.join(file_path, file)
            if os.path.isdir(file):
                cls.get_file(file)
            if file.split('.')[-1] not in ['yml', 'yaml'] or len(file.split('tmp')) > 1:
                continue
            else:
                cls.case_file_list.append(file)


if __name__ == '__main__':
    tmp = ReadFile()
    tmp.read_case_yml()
