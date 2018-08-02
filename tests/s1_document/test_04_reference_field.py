#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Define a reference field.


**中文文档**

Reference和Embedded Document不同的是, Embedded直接将子类以文档的形式嵌入在另一个
文档中。而Reference是将两个文档在两个Collection中分别保存, 然后在一个文档中引用
另一个文档。由于MongoDB没有Join功能, 所以使用Reference Document相当于实现了Join
功能。

当然单向引用或双向引用都是可以的, 但是这取决于具体的应用场景。

Ref: http://docs.mongoengine.org/guide/defining-documents.html?#reference-fields
"""

import pytest
from mongoengine import Document, fields
from learn_mongoengine.tests import client, db, reset_before_and_after


@reset_before_and_after
def test_one_to_one_with_reference_field():
    class User(Document):
        user_id = fields.IntField(primary_key=True)
        name = fields.StringField()

    class Post(Document):
        post_id = fields.IntField(primary_key=True)
        author = fields.ReferenceField(User)

    user = User(user_id=1, name="Jack")
    user.save()

    post = Post(post_id=1)
    post.author = user
    post.save()

    post = Post.objects.first()
    assert post.author.user_id == 1


@reset_before_and_after
def test_one_to_many_with_reference_field():
    class User(Document):
        user_id = fields.IntField(primary_key=True)
        name = fields.StringField()

    class Post(Document):
        post_id = fields.IntField(primary_key=True)
        authors = fields.ListField(fields.ReferenceField(User))

    jack = User(user_id=1, name="Jack").save()
    tom = User(user_id=2, name="Tom").save()
    paul = User(user_id=3, name="Paul").save()

    Post(post_id=1, authors=[jack, ]).save()
    Post(post_id=2, authors=[tom, ]).save()
    Post(post_id=3, authors=[paul, ]).save()
    Post(post_id=4, authors=[jack, tom]).save()
    Post(post_id=5, authors=[tom, paul]).save()
    Post(post_id=6, authors=[paul, jack]).save()
    Post(post_id=7, authors=[jack, tom, paul]).save()

    # Find all pages Jack is one of the author
    assert Post.objects(authors__in=[jack, ]).count() == 4

    # Find all pages that both Tome and Paul have authored
    assert Post.objects(authors__all=[tom, paul]).count() == 2

    # Remove Jack from the authors for a page.
    Post.objects().update(pull__authors=jack)
    for post_id, expected_n_authors in zip([1, 4, 6, 7], [0, 1, 1, 2]):
        post = Post.objects(post_id=post_id).get()
        assert len(post.authors) == expected_n_authors


@reset_before_and_after
def test_lazy_reference_field():
    class User(Document):
        user_id = fields.IntField(primary_key=True)
        name = fields.StringField()

    class Post(Document):
        post_id = fields.IntField(primary_key=True)
        author = fields.LazyReferenceField(User)

    user = User(user_id=1, name="Jack")
    user.save()

    post = Post(post_id=1)
    post.author = user
    post.save()

    post = Post.objects.first()

    # user_id not loaded yet
    with pytest.raises(AttributeError):
        post.author.user_id

    assert post.author.fetch().user_id == 1


# --- Dealing with deletion of referred documents ---
# http://docs.mongoengine.org/guide/defining-documents.html?#dealing-with-deletion-of-referred-documents

if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
