#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
``Document.objects`` 是一个 ``QuerySet`` 类, 和collection相似, ORM中的大部分操作
都是通过QuerySet来进行的。详细的API请参考:
http://docs.mongoengine.org/apireference.html#module-mongoengine.queryset

QuerySet可以当做Cursor来使用。与ResultSet相关的方法有:

Result related:

- :func:`get()`
- :func:`first()`
- :func:`all()`
- :func:`limit()`
- :func:`skip()`

Field related:

- :func:`only()`
- :func:`exclude()`
- :func:`all_fields()`

Ref: http://docs.mongoengine.org/guide/querying.html
"""

import pytest
from learn_mongoengine import run_if_is_main
from learn_mongoengine import config
from learn_mongoengine.s2_crud.p1_create import User


@run_if_is_main(__name__)
def insert_test_data():
    User.objects.insert([
        User(id=1, name="Jack"),
        User(id=2, name="Tom"),
        User(id=3, name="Paul"),
    ])

insert_test_data()


@run_if_is_main(__name__)
def get():
    """可预知结果有且只有一个时, 可以用此方法获得一个实例, 否则会抛出异常。
    """
    assert User.objects(id=1).get().id == 1
    with pytest.raises(Exception):
        user = User.objects.get()

get()


@run_if_is_main(__name__)
def first():
    """从 ``QuerySet`` 中取得第一个结果, 如果没有结果则返回 ``None``。该方法使用了
    Limit关键字, 所以当Match的文档很多时, 性能上是没有问题的。
    """
    assert User.objects().first().id == 1
    assert User.objects(id=4).first() is None  # Return None

first()


@run_if_is_main(__name__)
def all():
    """从 ``QuerySet`` 中取得所有结果的列表。如果没有结果则返回空列表。
    """
    assert len(User.objects().all()) == 3
    assert len(User.objects(id__gte=4).all()) == 0  # Return empty list

all()


@run_if_is_main(__name__)
def limit():
    """从 ``QuerySet`` 中取得前N个结果的列表。如果没有结果则返回空列表。
    请注意: 和pymongo不同的是, 当limit=0时, 返回第一条结果。
    """
    assert len(User.objects().limit(2)) == 2
    # When it is zero, return first one
    assert len(User.objects().limit(0)) == 1
    # When it is None, return all
    assert len(User.objects().limit(None)) == 3
    
    # no result fount
    assert len(User.objects(id__gte=4).limit(10)) == 0  # Return empty list
    
limit()


@run_if_is_main(__name__)
def skip():
    """从 ``QuerySet`` 中的结果中跳过前N个结果, 返回剩下结果的列表。
    如果没有结果则返回空列表。
    """
    query_set = User.objects().skip(1)
    assert [user.id for user in query_set] == [2, 3]

    assert len(User.objects().skip(3)) == 0

skip()
    

@run_if_is_main(__name__)
def only():
    """只返回某些field。给其他项赋值为 ``None``。当没有指定 ``_id`` 项时, 
    ``_id`` 项还是会返回。
    """
    assert User.objects().only("id").first().name is None
    assert User.objects().only("name").first().id == 1

only()


@run_if_is_main(__name__)
def exclude():
    """只忽略某些field, 返回剩下所有的。给其他项赋值为 ``None``。当忽略了
    ``_id`` 项时, 则返回的文档中的_id项为 ``None``。
    """
    assert User.objects().exclude("name").first().name is None
    assert User.objects().exclude("id").first().id is None

exclude()


@run_if_is_main(__name__)
def all_fields():
    """忽略之前only和exclude中所定义的, 返回所有项。
    """
    user = User.objects().exclude("name").all_fields().first()
    assert user.id == 1 and user.name == "Jack"

    user = User.objects().only("id").all_fields().first()
    assert user.id == 1 and user.name == "Jack"

all_fields()
