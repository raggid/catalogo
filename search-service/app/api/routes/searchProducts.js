
module.exports = app => {
  const controller = app.controllers.searchProducts;

  app.route('/products/search-products')
    .post(controller.searchProducts);
}