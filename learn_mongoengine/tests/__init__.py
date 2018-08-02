#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine

dbname = "devtest"
username = "admin"
password = "&2z7#tMH6BJt"


def connect_to_testdb():
    host = "mongodb://{username}:{password}@ds113063.mlab.com:13063/{dbname}". \
        format(username=username, password=password, dbname=dbname)
    client = mongoengine.connect(
        dbname,
        host=host,
    )
    client.drop_database(dbname)
    db = client[dbname]
    return client, db


client, db = connect_to_testdb()


def clear_all_data(db):
    for col_name in db.list_collection_names():
        if col_name != "system.indexes":
            col = db.get_collection(col_name)
            col.remove({})


def reset_before_and_after(func):
    def wrapper(*args, **kwargs):
        clear_all_data(db)
        func(*args, **kwargs)
        clear_all_data(db)

    return wrapper
