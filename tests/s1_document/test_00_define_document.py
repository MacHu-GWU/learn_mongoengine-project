#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mongoengine
from learn_mongoengine.tests import client, db


class User(mongoengine.Document):
    user_id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField(max_length=32)

    # 若不指定meta, 则默认使用default database, collection name是类名的小写
    meta = {
        "db_alias": "default",  # 定义所属的Database
        "collection": "user",  # 定义所属的Collection
    }


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
