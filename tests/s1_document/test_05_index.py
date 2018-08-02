#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
如何创建Index。

Ref: http://docs.mongoengine.org/guide/defining-documents.html?#indexes
"""

import pytest
from mongoengine import Document, fields
from learn_mongoengine.tests import client, db, reset_before_and_after


class Page(Document):
    category = fields.IntField()
    title = fields.StringField()
    rating = fields.StringField()
    created = fields.DateTimeField()

    meta = {
        "indexes": [
            "$title",  # text index
        ]
    }


page = Page().save()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
