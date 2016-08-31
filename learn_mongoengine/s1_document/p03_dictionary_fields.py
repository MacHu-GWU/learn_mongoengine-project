#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Define a dictionary field.


**中文文档**

dictionary fields是指直接以dictionary的形式存在, 而不需要ORM的项。这一点区别于
embedded document field。

Ref: http://docs.mongoengine.org/guide/defining-documents.html?highlight=index#dictionary-fields
"""

from learn_mongoengine import mongoengine


class Person(mongoengine.Document):
    person_id = mongoengine.IntField(primary_key=True)
    profile = mongoengine.DictField()
    

Person.objects.delete()


def test_dict_field():
    """
    """
    person = Person(person_id=1, profile={"name": "Jack"})
    person.save()
    
    person = Person.objects.first()
    assert isinstance(person.profile, dict) # is a dictionary
    
    
if __name__ == "__main__":
    """
    """
    test_dict_field()