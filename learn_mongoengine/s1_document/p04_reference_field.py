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

from learn_mongoengine import mongoengine, run_if_is_main


def reset_before_and_after(func):
    def wrapper(*args, **kwargs):
        User.objects.delete()
        Post.objects.delete()
        
        func(*args, **kwargs)
        
        User.objects.delete()
        Post.objects.delete()
    return wrapper


#--- test_reference_field ---
class User(mongoengine.Document):
    user_id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()
    

class Post(mongoengine.Document):
    post_id = mongoengine.IntField(primary_key=True)
    author = mongoengine.ReferenceField(User)


@reset_before_and_after
@run_if_is_main(__name__)
def test_reference_field():
    """
    """
    user = User(user_id=1, name="Jack")
    user.save()
    
    post = Post(post_id=1)
    post.author = user
    post.save()
    
    post = Post.objects.first()
    assert post.author.user_id == 1
    
test_reference_field()
    

#--- test_one_to_many_with_reference_field ---
class User(mongoengine.Document):
    user_id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()
    

class Post(mongoengine.Document):
    post_id = mongoengine.IntField(primary_key=True)
    authors = mongoengine.ListField(mongoengine.ReferenceField(User))
    
    
@reset_before_and_after
@run_if_is_main(__name__)
def test_one_to_many_with_reference_field():
    jack = User(user_id=1, name="Jack").save()
    tom = User(user_id=2, name="Tom").save()
    paul = User(user_id=3, name="Paul").save()
    
    Post(post_id=1, authors=[jack,]).save()
    Post(post_id=2, authors=[tom,]).save()
    Post(post_id=3, authors=[paul,]).save()
    Post(post_id=4, authors=[jack, tom]).save()
    Post(post_id=5, authors=[tom, paul]).save()
    Post(post_id=6, authors=[paul, jack]).save()
    Post(post_id=7, authors=[jack, tom, paul]).save()
    
    
    # Find all pages Jack is one of the author
    assert Post.objects(authors__in=[jack,]).count() == 4
    
    # Find all pages that both Tome and Paul have authored
    assert Post.objects(authors__all=[tom, paul]).count() == 2
    
    # Remove Jack from the authors for a page.
    Post.objects().update(pull__authors=jack)
    for post_id, expected_n_authors in zip([1, 4, 6, 7], [0, 1, 1, 2]):
        post = Post.objects(post_id=post_id).get()
        assert len(post.authors) == expected_n_authors
       
test_one_to_many_with_reference_field()
    
    
#--- Dealing with deletion of referred documents ---
# http://docs.mongoengine.org/guide/defining-documents.html?#dealing-with-deletion-of-referred-documents
