#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.1"
__short_description__ = "Learn MongoEngine, the MongoDB Backed ORM."
__license__ = "MIT"

try:
    from .connect import mongoengine
except:
    from learn_mongoengine import mongoengine