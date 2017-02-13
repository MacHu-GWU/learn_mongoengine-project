#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.1"
__short_description__ = "Learn MongoEngine, the MongoDB Backed ORM."
__license__ = "MIT"

try:
    from .connect import mongoengine
    from .pkg.decorator import run_if_is_main
except:
    from learn_mongoengine.connect import mongoengine
    from learn_mongoengine.pkg.decorator import run_if_is_main