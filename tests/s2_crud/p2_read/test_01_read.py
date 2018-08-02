#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Read即读取文档, 也叫查询, 在MongoDB中叫Query。

在Orm中, 通常我们不会用到特别复杂的查询, 而MongoEngine有一套比较完整的查询语法
对应着MongoDB的查询。而在用户需要更复杂的查询, 但是MongoEngine又没有提供相关
语法的情况下, 可以使用原生的raw query。

Ref: http://docs.mongoengine.org/guide/querying.html
"""

import pytest
from datetime import datetime
import mongoengine as me
from mongoengine.errors import DoesNotExist
from learn_mongoengine.tests import client, db, reset_before_and_after


class User(me.EmbeddedDocument):
    id = me.IntField(primary_key=True)
    name = me.StringField()


class Post(me.Document):
    id = me.IntField(primary_key=True)
    title = me.StringField()
    author = me.EmbeddedDocumentField(User)
    create_time = me.DateTimeField()
    tags = me.ListField(me.StringField())

    meta = {"db_alias": "default", "collection": "post"}


def insert_testdata():
    post = Post(
        id=1,
        title="Hello World!",
        author=User(id=1, name="Jack"),
        create_time=datetime(2002, 9, 11, 8, 30, 0),
        tags=["New User", "Student", "Room Rental", "Make Friend"]
    )
    post.save()


@reset_before_and_after
def test_basic_query():
    insert_testdata()

    # --- all documents ---
    assert len(Post.objects()) == 1
    assert len(Post.objects().all()) == 1
    assert len(list(Post.objects())) == 1

    # --- embedded document ---
    # use field1__field2 represent field1.field2
    assert Post.objects(author__name="Jack").get().id == 1

    # --- string query ---
    # http://docs.mongoengine.org/guide/querying.html#string-queries
    # exact
    assert Post.objects(title__exact="Hello World!").get().id == 1
    with pytest.raises(DoesNotExist):
        assert Post.objects(title__exact="HELLO WORLD!").get().id == 1

    # iexact
    assert Post.objects(title__iexact="HELLO WORLD!").get().id == 1

    # contains
    assert Post.objects(title__contains="Wor").get().id == 1
    with pytest.raises(DoesNotExist):
        assert Post.objects(title__contains="WOR").get().id == 1

    # icontains
    assert Post.objects(title__icontains="WOR").get().id == 1

    # startswith
    assert Post.objects(title__startswith="Hello").get().id == 1
    with pytest.raises(DoesNotExist):
        assert Post.objects(title__startswith="HELLO").get().id == 1

    # istartswith
    assert Post.objects(title__istartswith="HELLO").get().id == 1

    # endswith
    assert Post.objects(title__endswith="World!").get().id == 1
    with pytest.raises(DoesNotExist):
        assert Post.objects(title__endswith="WORLD!").get().id == 1

    # iendswith
    assert Post.objects(title__iendswith="WORLD!").get().id == 1


@reset_before_and_after
def test_querying_lists():
    """

    Ref: http://docs.mongoengine.org/guide/querying.html#querying-lists
    """
    insert_testdata()

    assert Post.objects(tags__1="Student").get().id == 1

    post = Post.objects.fields(slice__tags=[2, 3]).first()
    assert post.tags == ["Room Rental", "Make Friend"]


@reset_before_and_after
def test_raw_query():
    """
    有的时候过于复杂的query我们无法用mongoengine的Query API来表达, 这时候我们
    可以用原生的MongoDB Query API进行查询, 但是自动将返回的文档转化为对象。
    """
    insert_testdata()

    filters = {
        "_id": {"$gte": 1},
        "title": {"$regex": "^Hello"},
        "author.name": "Jack",
        "create_time": {"$lte": datetime(2016, 1, 1)},
    }
    assert Post.objects(__raw__=filters).get().id == 1


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
