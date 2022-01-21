from odoo import http, _
from odoo.http import request
from odoo.addons.sale.controllers.portal import CustomerPortal


class Main(CustomerPortal):

    @http.route(['/test/orders'], type='http', auth="user", website=True)
    def portal_my_orders(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = {}
        return request.render("my_library.test_portal_template", values)
