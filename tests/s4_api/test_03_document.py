#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Use pymongo.collection.Collection
=================================
有时候我们希望使用我们熟悉的pymongo API, :func:`get_collection_db()` 给出了
如何从mongoengine的Schema中获得Collection和Database的实例的方法。
"""

import pytest
from pymongo.database import Database
from pymongo.collection import Collection
import mongoengine as me
from learn_mongoengine.tests import client, db, reset_before_and_after


class User(me.Document):
    user_id = me.IntField(primary_key=True)
    name = me.StringField()


User(user_id=1, name="Jack").save()


def test_get_collection():
    """
    ``Document._get_collection()``, get ``pymongo.collection.Collection`` instance.
    """
    col_user = User._get_collection()
    assert isinstance(col_user, Collection)


def test_get_db():
    """
    ``Document._get_db()``, get ``pymongo.database.Database`` instance.
    """
    db_test = User._get_db()  # Get pymongo.database.Database instance
    assert isinstance(db_test, Database)


def test_get_id_field_name():
    """
    Access ``_id`` field attribute name:

    - ``Document.id.name``
    - ``Document._meta["id_field"]
    """
    assert User.id.name == "user_id"
    assert User._meta["id_field"] == "user_id"


def test_get_field_name_list_in_order():
    """
    Get field name list in order.

    **中文文档**

    获得已定义的所有项的名称, 顺序等同于定义时的顺序.
    """
    assert User._fields_ordered == ("user_id", "name")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
