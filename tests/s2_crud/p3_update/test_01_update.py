#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Update即更新。
"""

import pytest
import mongoengine as me
from learn_mongoengine.tests import client, db, reset_before_and_after


class User(me.Document):
    _id = me.IntField(primary_key=True)
    name = me.StringField()


@reset_before_and_after
def test_not_atomic_update():
    """
    第一种常用的update操作是直接获取多个实例, 然后对实例进行修改之后, 调用
    ``.save()`` 方法。这种做法实际上是删除了数据库中的实例, 然后插入一个新的实例。

    这样做有一个潜在的问题, 当多个客户端和服务端通信时, 如果客户端使用这种代码, 
    那么将无法保证数据库的原子性。因为可能有多个客户端同时修改了同一条文档。

    所以, 为了保证原子性, 应使用QuerySet的update方法。

    在开发者自己理解的开发模式下, 可以忽略此问题。
    """
    User.objects.insert(User(_id=1, name="Jack"))

    user = User.objects(_id=1).get()
    user.name = "Mike"
    user.save()

    assert User.objects(_id=1).get()["name"] == "Mike"


@reset_before_and_after
def test_atomic_update():
    """第二种方法是社区所推荐的方法, 能保证原子性。
    """
    User.objects.insert([
        User(_id=2, name="Tom"),
        User(_id=3, name="Paul"),
    ])

    # .update是multi update, 如果只update一条, 可以用update_one
    User.objects(_id__gte=2, _id__lte=3).update(name="Mike")

    assert User.objects(_id=2).get().name == "Mike"
    assert User.objects(_id=3).get().name == "Mike"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
