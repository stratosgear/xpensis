# -*- coding: utf-8 -*-
"""User models."""
from datetime import datetime

from elasticsearch_dsl import DocType, String, Date, Boolean, Float


class Trx(DocType):
    type = String()
    account = String()
    created_date = Date()
    amount = Float()
    trx_date = Date()
    
    class Meta:
        index = 'flexpenses'

    def save(self, ** kwargs):
        if not self.created_date:
            self.created_date = datetime.now()
        return super(Trx, self).save(kwargs)
