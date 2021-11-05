#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: wzy
@file: base_requests.py
@ide: PyCharm
@time: 2021/8/31
"""

import requests
import json
from tools import allure_step, allure_title, logger, allure_step_no
from tools.data_process import DataProcess


class BaseRequest(object):
    session = None

    @classmethod
    def get_session(cls):
        """
        单例模式保证测试过程中使用的都是一个session对象
        :return:
        """
        if cls.session is None:
            cls.session = requests.Session()
        return cls.session

    @classmethod
    def send_request(cls, case: dict, env: str = 'dev') -> object:
        """处理case数据，转换成可用数据发送请求
        :param case: yml读取单个用例数据，dict格式
        :param env: 环境名称 默认使用config.yaml server下的 dev 后面的基准地址
        return: 响应结果， 预期结果
        """
        data = str(case.get('data')) if case.get('data') else ''
        extractor = str(case.get('extractor')) if case.get('extractor') else ''
        logger.debug(
            f"用例进行处理前数据: \n 接口路径: {case['url']} \n 请求参数: {data} \n "
            f" 提取参数: {extractor} \n "
            f"预期结果: {case['validate']} \n ")
        # allure报告 用例标题
        allure_title(case['name'])
        # 处理url、header、data、file、的前置方法
        url = DataProcess.handle_path(case['url'], env)
        header = case.get('header') if case.get('header') else {}
        data = DataProcess.handle_data(data)
        allure_step('请求数据', str(data))
        file = None
        if case.get('file'):
            file, file_header = DataProcess.handler_files(case.get('file'), data)
            header.update(file_header)
            data = file
        header = DataProcess.handle_header(str(header))
        logger.info(file)
        # 发送请求
        response = cls.send_api(url, case['method'], case['paramType'], header, data)
        # 提取参数
        DataProcess.handle_extra(extractor, response)
        return response, str(case['validate'])

    @classmethod
    def send_api(
            cls,
            url,
            method,
            parametric_key,
            header=None,
            data=None,
            file=None) -> dict:
        """
        :param method: 请求方法
        :param url: 请求url
        :param parametric_key: 入参关键字， params(查询参数类型，明文传输，一般在url?参数名=参数值), data(一般用于form表单类型参数)
        json(一般用于json类型请求参数)
        :param data: 参数数据，默认等于None
        :param file: 文件对象
        :param header: 请求头
        :return: 返回res对象
        """
        session = cls.get_session()

        if parametric_key == 'params':
            res = session.request(
                method=method,
                url=url,
                params=data,
                headers=header)
        elif parametric_key == 'data':
            res = session.request(
                method=method,
                url=url,
                data=data,
                files=file,
                headers=header)
        elif parametric_key == 'json':
            res = session.request(
                method=method,
                url=url,
                json=data,
                files=file,
                headers=header)
        else:
            raise ValueError(
                '可选关键字为params, json, data')
        try:
            response = res.json()
        except json.JSONDecodeError:
            response = res.content
        logger.info(
            f'\n最终请求地址:{res.url}\n请求方法:{method}\n请求头:{header}\n请求参数:{data}\n上传文件:{file}\n响应数据:{response}')
        allure_step_no(f'响应耗时(s): {res.elapsed.total_seconds()}')
        allure_step('响应结果', response)
        return response
