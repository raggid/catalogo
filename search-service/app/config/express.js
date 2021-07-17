const express = require('express');
const bodyParser = require('body-parser');
const config = require('config');
const { Client } = require('@elastic/elasticsearch');
const consign = require('consign')
const cors = require('cors')
const helmet = require('helmet')

module.exports = () => {
  const app = express();
  const client = new Client({
    node: config.get('elasticsearch.host')
  });

  // SETANDO VARIÁVEIS DA APLICAÇÃO
  app.set('port', process.env.PORT || config.get('server.port'));
  app.set('esClient', client);

  // MIDDLEWARES
  app.use(bodyParser.json());
  app.use(cors());
  app.use(helmet());

  //ENDPOINTS
  consign({ cwd: 'api' })
    .then('controllers')
    .then('routes')
    .into(app);

  return app;
};