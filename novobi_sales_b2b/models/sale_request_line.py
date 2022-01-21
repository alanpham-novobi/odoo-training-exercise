from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleRequestLine(models.Model):
    _name = 'sale.request.line'
    _description = 'Sales Request Line'
    _order = 'request_id desc, sequence, id desc'
    _check_company_auto = True

    request_id = fields.Many2one('sale.request', string='Request Reference',
                                 required=True, ondelete='cascade', index=True, copy=False)
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Text(string='Description')
    product_id = fields.Many2one(
        'product.product', string='Product',
        change_default=True, ondelete='restrict')
    currency_id = fields.Many2one(related='request_id.currency_id', depends=[
                                  'request_id.currency_id'], store=True, string='Currency')
    company_id = fields.Many2one(
        related='request_id.company_id', string='Company', store=True, index=True)
    price_unit = fields.Float(
        'Unit Price', required=True, digits='Product Price', compute='_compute_price_unit')
    product_uom_qty = fields.Float(
        string='Demand Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    approve_product_qty = fields.Float(
        string='Approve Quantity', digits='Product Unit of Measure'
    )
    price_subtotal = fields.Monetary(
        compute='_compute_amount', string='Subtotal', store=True)

    @api.depends('approve_product_qty', 'price_unit', 'currency_id')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * line.approve_product_qty
            line.update({
                'price_subtotal': price
            })

    @api.depends('product_id', 'request_id.pricelist_id')
    def _compute_price_unit(self):
        for record in self:
            record.update({
                'price_unit': record.product_id.with_context(pricelist=self.request_id.pricelist_id.id).price
            })

    @api.onchange('approve_product_qty')
    def _onchange_product_qty(self):
        self.ensure_one()
        if self.approve_product_qty > self.product_uom_qty:
            raise UserError(
                _('Invalid approve quantity. Approve quantity must be smaller or equal to demand quantity'))
