#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ref: http://docs.mongoengine.org/guide/defining-documents.html?#document-inheritance
"""

from learn_mongoengine import mongoengine


#--- Document Inheritance ---
def test_document_inheritance():
    """If you want to put relative items in the same collection because they
    have common attributes and methods. You should use document inheritance.
    """
    class Item(mongoengine.Document):
        id = mongoengine.IntField(primary_key=True)
        
        meta = {"allow_inheritance": True}
        
    # SubClass doc is in it's super class collection
    class Music(Item):
        title = mongoengine.StringField()
        
        
    class Movie(Item):
        title = mongoengine.StringField()
        
    
    music = Music(id=1, title="I love you like the movies").save()
    movie = Movie(id=2, title="The Matrix").save()
    assert Item.objects.count() == 2
    
    
if __name__ == "__main__":
    """
    """
    test_document_inheritance()
    
    
#--- Abstract Classes ---
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
    
    
if __name__ == "__main__":
    """
    """
    test_abstract_classes()