#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Update即更新。
"""

from learn_mongoengine import mongoengine, run_if_is_main
from learn_mongoengine.s2_crud.p1_create import User


@run_if_is_main(__name__)
def not_atomic_update():
    """第一种常用的update操作是直接获取多个实例, 然后对实例进行修改之后, 调用
    ``.save()`` 方法。这种做法实际上是删除了数据库中的实例, 然后插入一个新的实例。
    
    这样做有一个潜在的问题, 当多个客户端和服务端通信时, 如果客户端使用这种代码, 
    那么将无法保证数据库的原子性。因为可能有多个客户端同时修改了同一条文档。
    
    所以, 为了保证原子性, 应使用QuerySet的update方法。
    
    在开发者自己理解的开发模式下, 可以忽略此问题。
    """
    User.objects.insert(User(id=1, name="Jack"))
    
    user = User.objects(id=1).get()
    user.name = "Mike"
    user.save()
    
    assert User.objects(id=1).get()["name"] == "Mike"

not_atomic_update()
    

@run_if_is_main(__name__)
def atomic_update():
    """第二种方法是社区所推荐的方法, 能保证原子性。
    """
    User.objects.insert([
        User(id=2, name="Tom"),
        User(id=3, name="Paul"),
    ])
    
    # .update是multi update, 如果只update一条, 可以用update_one
    User.objects(id__gte=2, id__lte=3).update(name="Mike")
    
    assert User.objects(id=2).get().name == "Mike"
    assert User.objects(id=3).get().name == "Mike"

atomic_update()