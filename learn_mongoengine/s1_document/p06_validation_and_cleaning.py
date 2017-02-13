#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
如何作validation。

Ref: http://docs.mongoengine.org/guide/document-instances.html#pre-save-data-validation-and-cleaning
"""

from datetime import datetime
from learn_mongoengine import mongoengine, run_if_is_main


class Essay(mongoengine.Document):
    status = mongoengine.StringField(choices=("Published", "Draft"), required=True)
    pub_date = mongoengine.DateTimeField()
    
    # clean() will be triggered on save()
    def clean(self):
        """Ensures that only published essays have a `pub_date` and
        automatically sets the pub_date if published and not set"""
        if self.status == "Draft" and self.pub_date is not None:
            msg = "Draft entries should not have a publication date."
            raise mongoengine.ValidationError(msg)
        # Set the pub_date for published items if not set.
        if self.status == "Published" and self.pub_date is None:
            self.pub_date = datetime.now()


@run_if_is_main(__name__)
def test():
    try:
        essay = Essay(status="Draft", pub_date=datetime.now())
        essay.save()
        raise Exception("mongoengine.ValidationError not raised!")
    except mongoengine.ValidationError:
        pass
    
    essay = Essay(status="Published")
    assert essay.pub_date is None
    essay.save()
    assert essay.pub_date is not None
    
test()