# encoding:utf-8

from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['eshost'],
    http_auth=('elastic', 'password'),
    port=80
)
