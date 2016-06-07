from datetime import datetime

from elasticsearch.client import Elasticsearch
import flask

from flaskexpenses.transactions.utils import find_oldest_trx_date_and_sum
from flaskexpenses.transactions.views import blueprint


client = Elasticsearch()

@blueprint.route('/ajax/daily_balance',  methods=['GET', 'POST'])
def ajax_daily_balance():
    
    oldest_date, starting_balance = find_oldest_trx_date_and_sum()
    
    # one day after
    oldest_date += 86400000
    
    
    response = client.search(index="flexpenses",
               body=
        {
  "query": {
    "filtered": {
      "query": {
        "query_string": {
          "query": "*",
          "analyze_wildcard": True
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "trx_date": {
                  "gte": oldest_date,
                  "format": "epoch_millis"
                }
              }
            }
          ],
          "must_not": []
        }
      }
    }
  },
  "size": 0,
  "aggs": {
    "theDates": {
      "date_histogram": {
        "field": "trx_date",
        "interval": "1d",
        "min_doc_count": 1,
        "extended_bounds": {
          "min": oldest_date
        }
      },
      "aggs": {
        "theSum": {
          "sum": {
            "field": "amount"
          }
        }
      }
    }
  }
})

    reply =  {
              "label": "Daily Balance",
              #"data": [[1999, 3.0], [2000, 3.9], [2001, 2.0], [2002, 1.2], [2003, 1.3], [2004, 2.5], [2005, 2.0], [2006, 3.1], [2007, 2.9], [2008, 0.9]]
              }
    data = []
    
    balance = starting_balance
    for bucket in response['aggregations']['theDates']['buckets']:
        point = []
        #unix_time = bucket['key'] / 1000.0
        #point.append(str(datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')))
        point.append(bucket['key'])
        balance += bucket['theSum']['value']
        point.append(balance)
        
        data.append(point)
    
    reply['data'] = data
    
    #>>> import datetime
    #>>> s = 1236472051807 / 1000.0
    #>>> datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
    #'2009-03-08 09:27:31.807000'

    return flask.jsonify(**reply)