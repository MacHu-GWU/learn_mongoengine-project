#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Define a embedded document field.

**中文文档**

Embedded document field是指field本身也需要ORM, 而不仅仅是作为一个字典存在。
请注意Embedded Document和Reference Document之间的区别。
"""

from learn_mongoengine import mongoengine


class User(mongoengine.EmbeddedDocument):
    user_id = mongoengine.IntField()
    name = mongoengine.StringField()
    

class Comment(mongoengine.EmbeddedDocument):
    author_id = mongoengine.IntField()
    content = mongoengine.StringField()


class Post(mongoengine.Document):
    post_id = mongoengine.IntField(primary_key=True)
    author = mongoengine.EmbeddedDocumentField(User)
    comments = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Comment))
    
Post.objects.delete()


def test_embedded_document():
    """
    """
    user = User(user_id=1, name="Jack")
    post = Post(
        post_id=1,
        author=user,
        comments=[
            Comment(author_id=1, content="This is my first post."),
            Comment(author_id=2, content="Nice post!")
        ],
    )
    post.save()
    
    post = Post.objects.first()
    assert isinstance(post.author, User) # is a User instance
    assert isinstance(post.comments[0], Comment) # is a Comment instance
    
    doc = Post._get_collection().find_one()
    assert doc == {
        '_id': 1, 
        'author': {'user_id': 1, 'name': 'Jack'},
        'comments': [
            {'author_id': 1, 'content': 'This is my first post.'}, 
            {'author_id': 2, 'content': 'Nice post!'},
        ],
    }


if __name__ == "__main__":
    """
    """
    test_embedded_document()