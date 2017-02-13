#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Use pymongo.collection.Collection
=================================
有时候我们希望使用我们熟悉的pymongo API, :func:`get_collection_db()` 给出了
如何从mongoengine的Schema中获得Collection和Database的实例的方法。
"""

from learn_mongoengine import run_if_is_main
from learn_mongoengine.s2_crud.p1_create import User


def get_collection_db():
    """获取Collection和Database的实例。
    """
    User(id=1, name="Jack").save()
    # Get pymongo.collection.Collection instance
    user_col = User._get_collection()
    doc = user_col.find_one()
    assert doc == {"_id": 1, "name": "Jack"}

    test_db = User._get_db()  # Get pymongo.database.Database instance

get_collection_db()
