#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delete即删除。

在MongoEngine中我们有两种方法可以删除文档。

1. 调用实例的 ``.delete()`` 方法。
2. 对 `QuerySet <http://docs.mongoengine.org/apireference.html?highlight=delete#mongoengine.queryset.QuerySet>`_
  调用 `delete() <http://docs.mongoengine.org/apireference.html?highlight=delete#mongoengine.queryset.QuerySet.delete>`_ 
  方法。等效于 ``collection.remove(query)``。
"""

import pytest
import mongoengine as me
from learn_mongoengine.tests import client, db, reset_before_and_after


class User(me.Document):
    _id = me.IntField(primary_key=True)
    name = me.StringField()


@reset_before_and_after
def test_delete_one_document():
    """
    两种delete文档的方法的例子。
    """
    User.objects.insert([User(_id=i) for i in [1, 2, 3]])
    assert User.objects.count() == 3

    # 1. Delete from instance
    # Delete _id == 1
    user = User(_id=1)
    user.delete()
    assert User.objects.count() == 2

    # 2. Delete from a query
    # Delete _id >= 2
    User.objects(_id__gte=2).delete()
    assert User.objects.count() == 0


@reset_before_and_after
def test_remove_all_document():
    """
    Remove all document.
    """
    User.objects.insert([User(_id=i) for i in range(10)])
    assert User.objects.count() == 10

    # Delete all document, but not index
    User.objects.delete()
    assert User.objects.count() == 0


@reset_before_and_after
def test_drop_collection():
    """
    Drop collection. And also remove index data.
    """
    # Drop Collection
    User.drop_collection()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
