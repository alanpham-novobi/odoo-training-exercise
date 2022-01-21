odoo.define('novobi_sales_b2b.CreateSaleRequest', function (require) {
  var core = require('web.core');
  $('.create-sale-request').click(function () {
    window.location.href = '/my/b2b-admin/orders/create';
  })
});