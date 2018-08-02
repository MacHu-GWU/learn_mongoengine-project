#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Representing inheritance in the database
There are three ways to implement inheritance in the database:

Single Table Inheritance: all entities in the hierarchy are mapped to a single database table.
Class Table Inheritance: each entity in the hierarchy is mapped to a separate table, but each table stores only the attributes which the entity doesn’t inherit from its parents.
Concrete Table Inheritance: each entity in the hierarchy is mapped to a separate table and each table stores the attributes of the entity and all its ancestors.

Ref: http://docs.mongoengine.org/guide/defining-documents.html?#document-inheritance
"""

import pytest
from mongoengine import Document, fields
from learn_mongoengine.tests import client, db, reset_before_and_after


#--- Document Inheritance ---
@reset_before_and_after
def test_document_inheritance():
    """
    If you want to put relative items in the same collection because they
    have common attributes and methods. You should use document inheritance.

    请注意, inheritance在数据库中的实现是, 所有继承于一个母文档的子文档实际
    都放在一个collection下, mongoengine通过加前缀的方式, 将其区分开来。所以
    如果你只是想继承属性和方法, 那么你应该使用 ``{"abstract": True}``。
    """
    class Item(Document):
        id = fields.IntField(primary_key=True)

        meta = {"allow_inheritance": True}

    # SubClass doc is in it's super class collection
    class Music(Item):
        title = fields.StringField()

    class Movie(Item):
        title = fields.StringField()

    # id for different subclass has to be different
    music = Music(id=1, title="I love you like the movies").save()
    movie = Movie(id=2, title="The Matrix").save()
    assert Item.objects.count() == 2

    music = Music.objects().first()
    assert music.to_mongo().to_dict()["_cls"] == "Item.Music"

    movie = Movie.objects().first()
    assert movie.to_mongo().to_dict()["_cls"] == "Item.Movie"


#--- Abstract Classes ---
@reset_before_and_after
def test_abstract_classes():
    """很多时候我们会觉得mongoengine.Document提供的方法不够多, 我们会想要自定义
    一些方法。为了减少冗余代码, 我们想要将通用的方法以继承的方式实现。这时, 我们
    需要建立一个新的Document的基类, 然后用户的类都从这个基类继承而来。

    具体做法如下:

    Ref: http://docs.mongoengine.org/guide/defining-documents.html?#abstract-classes
    """
    class ExtendedDocument(Document):
        # abstract = True
        meta = {
            "abstract": True,
        }

        def keys(self):
            return list(self._fields_ordered)

    class User(ExtendedDocument):
        id = fields.IntField(primary_key=True)
        name = fields.StringField()

    User.objects.delete()
    user = User(id=1).save()

    assert User.objects.count() == 1
    assert user.keys() == ["id", "name"]


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
