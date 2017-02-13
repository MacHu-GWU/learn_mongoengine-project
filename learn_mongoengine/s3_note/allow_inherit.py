#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ref: http://docs.mongoengine.org/guide/defining-documents.html?#document-inheritance
"""

from learn_mongoengine import mongoengine, run_if_is_main


#--- Document Inheritance ---
@run_if_is_main(__name__)
def test_document_inheritance():
    """If you want to put relative items in the same collection because they
    have common attributes and methods. You should use document inheritance.
    
    请注意, inheritance在数据库中的实现是, 所有继承于一个母文档的子文档实际
    都放在一个collection下, mongoengine通过加前缀的方式, 将其区分开来。所以
    如果你只是想继承属性和方法, 那么你应该使用 ``{"abstract": True}``。
    """
    class Item(mongoengine.Document):
        id = mongoengine.IntField(primary_key=True)
        
        meta = {"allow_inheritance": True}
        
    # SubClass doc is in it's super class collection
    class Music(Item):
        title = mongoengine.StringField()
        
        
    class Movie(Item):
        title = mongoengine.StringField()
        
    
    # id for different subclass has to be different
    music = Music(id=1, title="I love you like the movies").save()
    movie = Movie(id=2, title="The Matrix").save()
    assert Item.objects.count() == 2
    
    music = Music.objects().first()
    assert music.to_mongo().to_dict()["_cls"] == "Item.Music"
    
    movie = Movie.objects().first()
    assert movie.to_mongo().to_dict()["_cls"] == "Item.Movie"
    
test_document_inheritance()
    
    
#--- Abstract Classes ---
@run_if_is_main(__name__)
def test_abstract_classes():
    """很多时候我们会觉得mongoengine.Document提供的方法不够多, 我们会想要自定义
    一些方法。为了减少冗余代码, 我们想要将通用的方法以继承的方式实现。这时, 我们
    需要建立一个新的Document的基类, 然后用户的类都从这个基类继承而来。
    
    具体做法如下:
    
    Ref: http://docs.mongoengine.org/guide/defining-documents.html?#abstract-classes
    """
    class ExtendedDocument(mongoengine.Document):
        # abstract = True
        meta = {
            "abstract": True,
        }
        
        def keys(self):
            return list(self._fields_ordered)
    
    
    class User(ExtendedDocument):
        id = mongoengine.IntField(primary_key=True)
        name = mongoengine.StringField()
        
    
    User.objects.delete()
    user = User(id=1).save()
    
    assert User.objects.count() == 1
    assert user.keys() == ["id", "name"]
    
test_abstract_classes()