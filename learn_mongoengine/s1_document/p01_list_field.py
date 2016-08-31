#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Define a list field.
"""

from learn_mongoengine import mongoengine


class Item(mongoengine.Document):
    tags = mongoengine.ListField(mongoengine.StringField(max_length=50)) 