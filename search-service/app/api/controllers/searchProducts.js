module.exports = app => {
    const esClient = app.get('esClient');
    const controller = {};

    controller.searchProducts = async (req, res) => {
        let elasticResponse;
        try {
            elasticResponse = await esClient.search({
                index: 'product_index',
                body: {
                    "size": 50,
                    "query": {
                        "nested": {
                            "path": "searchContext",
                            "query": {
                                "multi_match": {
                                    "query": req.body['text'],
                                    "type": "cross_fields",
                                    "fields": [
                                        "searchContext.searchString^3",
                                        "searchContext.searchString.autocomplete",
                                        "searchContext.searchString.ngram",
                                        // "searchContext.years^4"
                                    ],
                                    "operator": "and"
                                }
                            }
                        }
                    }
                }
            })
        } catch (err) {
            console.log(err);
            res.status(400).json({ msg: "Falha ao realizar a busca", detail: err.message });
            return controller;
        }
        const elasticProducts = elasticResponse.body.hits.hits;
        console.log("Number of hits: " + elasticProducts.length)
        const products = elasticProducts.map(elasticProduct => {
            return {
                internalCode: elasticProduct._source.internalCode,
                masterCode: elasticProduct._source.masterCode,
                provider: elasticProduct._source.provider,
                description: elasticProduct._source.description,
                techSpecs: elasticProduct._source.techSpecs,
                // applications: elasticProduct._source.applications
            }
        })
        res.status(200).json(products);
    };

    return controller;
}