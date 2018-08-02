#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
如何作validation。

Ref: http://docs.mongoengine.org/guide/document-instances.html#pre-save-data-validation-and-cleaning
"""

import pytest
import mongoengine
from mongoengine import Document, fields
from datetime import datetime
from learn_mongoengine.tests import client, db, reset_before_and_after


class Essay(Document):
    status = fields.StringField(choices=("Published", "Draft"), required=True)
    pub_date = fields.DateTimeField()

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


@reset_before_and_after
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


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
