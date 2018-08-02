#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create即创建新文档, 在MongoDB中叫Insert。
"""

import pytest
import mongoengine as me
from learn_mongoengine.tests import client, db, reset_before_and_after


class User(me.Document):
    _id = me.IntField(primary_key=True)
    name = me.StringField()

    def __repr__(self):
        return "User(_id=%r, name=%r)" % (self._id, self.name)

    def __str__(self):
        return self.__repr__()


@reset_before_and_after
def test_basic_insert():
    """
    一次插入一条文档。

    请注意, 使用 instance.save() 方法进行Insert是一种错误的方式。    
    """
    User.objects.insert(User(_id=1, name="Jack"))

    user = User.objects(_id=1).get()
    assert user.name == "Jack"


@reset_before_and_after
def test_bulk_insert():
    """
    一次性插入多条文档。
    """
    User.objects.insert([User(_id=2, name="Tom"), User(_id=3, name="Paul")])

    user = User.objects(_id=2).get()
    assert user.name == "Tom"
    user = User.objects(_id=3).get()
    assert user.name == "Paul"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
