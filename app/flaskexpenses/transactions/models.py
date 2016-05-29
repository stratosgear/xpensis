# -*- coding: utf-8 -*-
"""User models."""
from datetime import datetime

from elasticsearch_dsl import DocType, String, Date, Boolean, Float


class Trx(DocType):
    type = String()
    account = String()
    created_at = Date()
    amount = Float()
    
    class Meta:
        index = 'flexpenses'


    def save(self, ** kwargs):
        self.created_at = datetime.now()
        return super(Trx, self).save(kwargs)
