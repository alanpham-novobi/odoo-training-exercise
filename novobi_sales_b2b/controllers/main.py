from odoo import http, fields
from odoo.http import request
import logging
from odoo.addons.sale.controllers.portal import CustomerPortal
logger = logging.getLogger(__name__)


class RequestController(CustomerPortal):
    # Create new sales request
    @http.route("/my/b2b-admin/create", type='json', auth='public', csrf=False, methods=['POST'])
    def create_request(self, **kw):
        record = request.env['sale.request'].sudo().create(kw)
        return record

    # Update sales request
    @http.route("/my/b2b-admin/update", type='json', auth='public', methods=['POST'])
    def update_sale_request(self, **kw):
        logger.info(kw)
        request_id = int(kw.get('id'))
        del kw['id']
        try:
            record = request.env['sale.request'].sudo().browse(request_id)
            record.update(kw)
            return "<h1>Success/<h1>"
        except Exception as e:
            logger.error(e)
            return "<h1>Something went wrong</h1>"

    # Cancel sales request
    @http.route("/my/b2b-admin/cancel", type='http', auth='public')
    def cancel_sale_request(self, request_id, **kw):
        try:
            record = request.env['sale.request'].sudo().browse(
                int(request_id))
            record.update({
                'request_state': 'cancelled',
                'date_confirm': fields.datetime.now(),
                'amount_total': 0.0
            })
            return "<h1>Success</h1>"
        except Exception as e:
            logger.error(e)
            return "<h1>Something went wrong</h1>"

    @http.route("/my/b2b-admin/cancel/<model('sale.request'):request>", type='http', auth='public')
    def cancel_sale_request_in_path(self, request):
        return self.cancel_sale_request(request.id)

    # Render sales request portal
    @http.route(['/my/b2b-admin/orders'], type='http', auth="public", website=True)
    def portal_order(self, **kw):
        try:
            sale_requests = request.env['sale.request'].search([])
            logging.info(sale_requests)
        except:
            return "<h1>Can't Access API</h1>"
        return request.render('novobi_sales_b2b.portal_sale_requests', {
            'requests': sale_requests
        })

    # Render detailed sales request portal
    @http.route('/my/b2b-admin/orders/details', type='http', auth='public', website=True)
    def sale_request_details(self, request_id):
        try:
            sale_request = request.env['sale.request'].sudo().browse(
                int(request_id))
            sale_request_lines = request.env['sale.request.line'].sudo().search(
                [('request_id', '=', int(request_id))]
            )
        except Exception as e:
            logger.error(e)
            return "<h1>Can't Access API</h1>"

        sale_order = None
        if sale_request:
            sale_order = request.env['sale.order'].sudo().browse(
                int(sale_request.order_id.id))
        return request.render('novobi_sales_b2b.portal_sale_request_detailed', {
            'sale_request': sale_request,
            'request_lines': sale_request_lines,
            'sale_order': sale_order
        })

    @http.route("/my/b2b-admin/orders/details/<model('sale.request'):request>", type='http', auth='public', website=True)
    def sale_request_details_in_path(self, request):
        return self.sale_request_details(request.id)

    # Create new request
    @http.route("/my/b2b-admin/orders/create", type='http', auth='public', website=True)
    def create_sale_request(self):
        products = request.env['product.product'].search([])
        return request.render('novobi_sales_b2b.create_sale_request_form', {
            'products': products
        })
