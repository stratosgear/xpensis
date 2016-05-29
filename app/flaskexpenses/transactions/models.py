# -*- coding: utf-8 -*-
"""User models."""
from datetime import datetime

from elasticsearch_dsl import DocType, String, Date, Boolean, Float


class Trx(DocType):
    type = String(index='not_analyzed')
    amount = Float()
    account = String(index='not_analyzed')
    account_type = String(index='not_analyzed')
    description = String()
    trx_date = Date()
    created_date = Date()
    tags = String(index='not_analyzed', multi=True)
    payee = String(index='not_analyzed')
    
    class Meta:
        index = 'flexpenses'

    def save(self, ** kwargs):
        if not self.created_date:
            self.created_date = datetime.now()
        return super(Trx, self).save(kwargs)
