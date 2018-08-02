#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Define a list field.
"""

import pytest
import mongoengine
from learn_mongoengine.tests import client, db


class Item(mongoengine.Document):
    tags = mongoengine.ListField(mongoengine.StringField(max_length=50))


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
