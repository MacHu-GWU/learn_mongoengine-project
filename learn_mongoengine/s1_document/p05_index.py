#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
如何创建Index。

Ref: http://docs.mongoengine.org/guide/defining-documents.html?#indexes
"""

from learn_mongoengine import mongoengine


class Page(mongoengine.Document):
    category = mongoengine.IntField() 
    title = mongoengine.StringField()
    rating = mongoengine.StringField()
    created = mongoengine.DateTimeField()
    
    meta = {
        "indexes": [
            "$title",  # text index
        ]
    }
    
page = Page().save()