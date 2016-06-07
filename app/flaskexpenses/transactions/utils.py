from elasticsearch.client import Elasticsearch

client = Elasticsearch()

def find_oldest_trx_date_and_sum():
    """
    {
  "size": 0,
  "query": {
    "match_all": {}
  },
  "aggs": {
    "3": {
      "terms": {
        "field": "trx_date",
        "size": 1,
        "order": {
          "_term": "asc"
        }
      }
    }
  }
}"""
    
    response = client.search(index="flexpenses",
               body=    {
  "size": 0,
  "query": {
    "match_all": {}
  },
  "aggs": {
    "theDate": {
      "terms": {
        "field": "trx_date",
        "size": 1,
        "order": {
          "_term": "asc"
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
    
    
    bucket = response['aggregations']['theDate']['buckets'][0]
    return bucket['key'], bucket['theSum']['value']


def get_total_balance():
    
    
    response = client.search(index="flexpenses",
               body={
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
              "query": {
                "query_string": {
                  "analyze_wildcard": True,
                  "query": "*"
                }
              }
            },
            {
              "range": {
                "trx_date": {
                  "gte": 1307394631564,
                  "lte": 1465247431564,
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
    "totbal": {
      "sum": {
        "field": "amount"
      }
    }
  }
})
    
    
    return response['aggregations']['totbal']['value']


def get_totals_per_account_type():
    
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
                  "gte": 1307398072443,
                  "lte": 1465250872445,
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
    "accType": {
      "terms": {
        "field": "account_type",
        "size": 5,
        "order": {
          "_term": "asc"
        }
      },
      "aggs": {
        "accSum": {
          "sum": {
            "field": "amount"
          }
        }
      }
    }
  }
})
    
    buckets = response['aggregations']['accType']['buckets']
    return buckets[0]['accSum']['value'], buckets[1]['accSum']['value'], buckets[2]['accSum']['value']
    
    