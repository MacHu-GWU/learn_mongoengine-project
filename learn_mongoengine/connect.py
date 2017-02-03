#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
mongoengine.connect方法实际上是为多个数据的连接建立一个连接池, 而各个连接之间
使用alias进行区分。

不同的数据对象不仅仅是对应不同的collection, 还可能对应不同的database。所以我们
要在connect中分别连接这些数据库, 并在meta中声明数据对象所属的数据库。官方文档
请参考: http://docs.mongoengine.org/guide/connecting.html#multiple-databases

Ref: http://docs.mongoengine.org/guide/connecting.html#guide-connecting
"""

import mongoengine
from learn_mongoengine import config

# Use real MongoDB
if not config.USE_MONGOMOCK:
    # Test database
    conn_test = mongoengine.connect(
        db="test", alias="default",
        username=None, password=None, host="localhost", port=27017,
    )
    conn_test.drop_database("test")
    
    # Dev database
    conn_dev = mongoengine.connect(
        db="dev", alias="dev",
        username=None, password=None, host="localhost", port=27017,
    )
    conn_dev.drop_database("dev")

# Use mongomock
else:
    conn_test = mongoengine.connect(
        db="test", alias="default", host="mongomock://localhost", 
        dbpath=config.MONGOMOCK_DBPATH,
    )
    conn_test.drop_database("test")
    
    conn_test = mongoengine.connect(
        db="dev", alias="dev", host="mongomock://localhost", 
        dbpath=config.MONGOMOCK_DBPATH,
    )
    conn_test.drop_database("dev")
