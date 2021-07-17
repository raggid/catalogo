from elasticsearch import Elasticsearch

from app.settings import ElasticSettings


def get_es_node():
    es_settings = ElasticSettings()
    es = Elasticsearch(es_settings.es_host)
    try:
        yield es
    finally:
        es.close()
