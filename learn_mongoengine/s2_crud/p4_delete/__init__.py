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

from learn_mongoengine.connect import mongoengine
from learn_mongoengine.s2_crud.p1_create import User


def delete_one_document():
    """两种delete文档的方法的例子。
    """
    User.objects.insert([User(id=i) for i in [1, 2, 3]])
    assert User.objects.count() == 3
 
    # Delete id == 1
    user = User(id=1)
    user.delete()
    assert User.objects.count() == 2
 
    # Delete id >= 2
    User.objects(id__gte=2).delete()
    assert User.objects.count() == 0


if __name__ == "__main__":
    """
    """
    delete_one_document()


def remove_all_document():
    """Remove all document.
    """
    User.objects.insert([User(id=i) for i in range(10)])
    assert User.objects.count() == 10
    
    # Delete all document, but not index
    User.objects.delete()
    assert User.objects.count() == 0
    

if __name__ == "__main__":
    """
    """
    remove_all_document()


def drop_collection():
    """Drop collection.
    """
    # Drop Collection
    User.drop_collection()
    
    
if __name__ == "__main__":
    """
    """
    drop_collection()