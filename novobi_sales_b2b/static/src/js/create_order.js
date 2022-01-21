odoo.define('novobi_sales_b2b.AddItemToRequest', function (require) {
    var core = require('web.core');
    var cart = [];
    console.log(cart)
    $('.add').click(function () {
        cart.push({
            "product_id": $('#product_id option:selected').val(),
            "product_oum_qty": $('#qty').val()
        })
        console.log(cart)
    })
});