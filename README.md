
## 实现功能
- 测试数据隔离: 测试前后进行数据库备份/还原
- 接口直接的数据依赖: 需要B接口使用A接口响应中的某个字段作为参数
- 对接数据库： 讲数据库的查询结果可直接用于断言操作
- 动态多断言： 可（多个）动态提取实际预期结果与指定的预期结果进行比较断言操作
- 自定义扩展方法： 在用例中使用自定义方法(如：获取当前时间戳...)的返回值 
- 邮件发送：将allure报告压缩后已附件形式发送
- 接口录制：录制指定包含url的接口,生成用例数据
## 依赖库
```
allure-pytest==2.8.17		# allure报告
jsonpath==0.82				# json解析库
loguru==0.5.1				# 日志库
pytest==6.0.1				# 参数化
PyYAML==5.3.1				# 读取ymal
requests==2.24.0			# 请求HTTP/HTTPS
xlrd==1.2.0					# 读取excel
yagmail==0.11.224			# 发送邮件
PyMySQL==0.10.1				# 连接mysql数据库
pytest-rerunfailures==9.1.1	# 用例失败重跑
paramiko==2.7.2				# SSH2 连接
xlwt==1.3.0                 # 写excel 用例文件
mitmproxy==6.0.2            # 抓包工具
```
## 目录结构
```shell
├─api
│  └─base_requests.py	# 请求封装
├─backup_sqls  
│  └─xxx.sql		# 数据库备份文件
├─config
│  └─config.yaml	# 配置文件
├─data
│  └─test_data.xlsx	# 用例文件
├─log
│  └─run...x.log	# 日志文件
├─report
│  ├─data
│  └─html			# allure报告
├─test
│  ├─conftest.py	# 依赖对象初始化
│  └─test_api.py	# 测试文件
├─tools		# 工具包
│  ├─__init__.py		# 常用方法封装
│  ├─data_clearing.py	# 数据隔离
│  ├─data_process.py	# 依赖数据处理
│  ├─db.py				# 数据库连接对象
│  ├─hooks.py			# 自定义扩展方法(可用于用例)文件 
│  ├─read_file.py		# 用例、配置项读取
│  ├─recording.py		# 接口录制,写入用例文件
│  └─send_email.py		# 邮件发送、报告压缩
├─项目实战接口文档.md	   # 配套项目相关接口文档
├─requirements.txt		 # 项目依赖库文件
└─run.py	# 主启动文件
```
## 更新 
####2021-11-03 
```
1. 支持yml/yaml 格式测试用例
2. 自动查找caseData目录下所有用例文件，多层目录支持
3. 支持根据tag运行测试用例，conftest.py文件传tag值
4. 数字工厂文件上传接口支持
```
####2021-11-04
```
1. 支持文件获取，报告显示附件图片
2. 支持嵌套参数化 如：url: bussiness-uc/api/${file_url("${fileUrl}")}
```

