PUT product_index
{
    "settings": {
        "index": {
            "number_of_shards": "3",
            "number_of_replicas": "0",
            "max_ngram_diff": 10,
            "analysis": {
                "filter": {
                    "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": "2",
                        "max_gram": "20"
                    },
                    "ngram_filter":{
                        "type": "ngram",
                        "min_gram": "3",
                        "max_gram": "10"
                    }
                    // "synonym_filter": {
                    //     "type": "synonym",
                    //     "synonyms_path": "/usr/share/elasticsearch/data/synonyms.txt"
                    //     // "updateable": true
                    // }
                },
                "analyzer": {
                    "autocomplete_analyzer": {
                        "filter": [
                            "lowercase",
                            "asciifolding",
                            // "synonym_filter",
                            "autocomplete_filter"
                        ],
                        "type": "custom",
                        "tokenizer": "whitespace"
                    },
                    // "synonym_analyzer": {
                    //     "filter": [
                    //         "lowercase",
                    //         "asciifolding",
                    //         "synonym_filter"
                    //     ],
                    //     "tokenizer": "whitespace"
                    // },
                    "ngram":{
                        "filter": [
                            "lowercase",
                            "asciifolding",
                            // "synonym_filter",
                            "ngram_filter"
                        ],
                        "tokenizer": "whitespace"                        
                    },
                    "whitespace_analyzer": {
                        "filter": [
                            "lowercase",
                            "asciifolding"
                        ],
                        "tokenizer": "whitespace"
                    }
                }
            }
        }
    },
    "mappings":{
        "dynamic": "false",
        "properties":{
            "internalCode":{"type": "text"},
            "masterCode": {"type": "text"},
            "brand":{"type": "text"},
            "brandSuffix":{"type": "text"},
            "description":{"type": "text"},
            "techSpecs": {
                "type": "nested",
                "properties": {
                    "name": { "type": "keyword"},
                    "value": { "type": "keyword"},
                    "unit" : { "type": "keyword"}
                }
            },
            "applications":{
                "type": "nested",
                "enabled": "false"
            },
            "searchContext":{
                "type": "nested",
                "properties":{
                    "searchString":{
                        "type": "text",
                        "analyzer": "standard",
                        "fields": {
                            "autocomplete": { 
                                "type": "text",
                                "analyzer": "autocomplete_analyzer",
                                "search_analyzer": "whitespace_analyzer"
                            },
                            "ngram": {
                                "type": "text",
                                "analyzer": "ngram",
                                "search_analyzer": "whitespace_analyzer"
                            },
                            "keyword":{
                                "type": "keyword"
                            }
                        }
                    },
                    "years":{
                        "type": "text",
                        "analyzer": "whitespace_analyzer"
                    }
                }
            }
        }
    }
}


GET product_index/_search
{
    "query": {
        "match_all": {}
    }
}

GET product_index/_search
{
    "query": {
        "nested": {
            "path": "searchContext",
            "query": {
                "multi_match": {
                    "query": "amort",
                    "type": "cross_fields",
                    "fields": [
                        "searchContext.searchString^3",
                        "searchContext.searchString.autocomplete",
                        "searchContext.searchString.ngram"
                        // "searchContext.years^4"
                    ],
                    "operator": "and"                    
                }
            }
        }
    }
}

POST _reindex
{
    "source": {
        "index": "products_5"
    },
    "dest": {
        "index": "products_1"
    }
}

POST /_aliases
{
  "actions" : [
    { "remove" : { "index" : "products_1", "alias" : "products_index" }},
    { "add" : { "index" : "products", "alias" : "products_index" } }
  ]
}