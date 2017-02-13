#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create即创建新文档, 在MongoDB中叫Insert。
"""

from learn_mongoengine import mongoengine, run_if_is_main


class User(mongoengine.Document):
    id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()
    
    def __repr__(self):
        return "User(id=%r, name=%r)" % (self.id, self.name)
    
    def __str__(self):
        return self.__repr__()
    

User.objects.delete()


@run_if_is_main(__name__)
def basic_insert():
    """一次插入一条文档。
    
    请注意, 使用 instance.save() 方法进行Insert是一种错误的方式。    
    """
    User.objects.insert(User(id=1, name="Jack"))
    
    user = User.objects(id=1).get()
    assert user.name == "Jack"

basic_insert()
    
    
@run_if_is_main(__name__)
def bulk_insert():
    """一次性插入多条文档。
    """
    User.objects.insert([User(id=2, name="Tom"), User(id=3, name="Paul")])
    
    user = User.objects(id=2).get()
    assert user.name == "Tom"
    user = User.objects(id=3).get()
    assert user.name == "Paul"
            
bulk_insert()