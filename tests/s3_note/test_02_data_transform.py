#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How to convert mongoengine.Document to generic python types?
============================================================
1. use example provided in :func:`to_keys_values_bson_dict_json`
2. query it using pymongo.Collection.
"""

import pytest
from mongoengine import Document, fields
from learn_mongoengine.tests import client, db, reset_before_and_after


@reset_before_and_after
def to_keys_values_bson_dict_json():
    """
    Convert Document to generic python types.
    """

    class User(Document):
        _id = fields.IntField()
        name = fields.StringField()

    user = User(_id=1, name="Jack")

    # to tuple
    assert user._fields_ordered == ("id", "name")

    # to keys
    assert list(user)

    # to values
    assert [getattr(user, key) for key in user] == [1, "Jack"]

    # to bson
    son = user.to_mongo()

    # to dict, key is DB document field, not Class field
    d = son.to_dict()
    assert d["_id"] == 1 and d["name"] == "Jack"

    # to json
    assert user.to_json() == '{"_id": 1, "name": "Jack"}'


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
