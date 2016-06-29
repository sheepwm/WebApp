#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
设计db模块的原因：
  1. 更简单的操作数据库
    一次数据访问：数据库连接=>游标对象=>执行SQL=>异常处理=>清理资源。
    db模块对这些过程进行封装，使得用户仅需关注SQL执行。
  2. 数据安全
    用户请求以多线程处理时，为了避免多线程下的数据共享引起的数据混乱，需要将数据连接以ThreadLocal对象传入
设计db接口：
  1. 设计原则：
    根据上层调用者设计简单易用的API接口
  2. 调用接口
    (1. 初始化数据库连接信息
    (2. 执行SQL DML
  3. 支持事物
"""

import time
import uuid
import functools
import threading
import logging

# global engine object
engine = None

# 数据库引擎对象
class _Engine(object):
    def __init__(self, connect):
        self._connect = connect
    def connect(self):
        return self._connect()
# 持有数据库连接的上下文对象
class _DbCtx(threading.local):
    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return not self.connection is none

    def init(self):
        self.connection = _LasyConnection()
        self.connections = 0

    def cleanup(self):
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        return self.connection.cursor()

_db_ctx = _DbCtx()
