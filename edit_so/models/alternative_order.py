from odoo import fields, models, api


class AlternativeOrder(models.Model):
    _name = 'alternative.order'

    product_id = fields.Many2one('product.product')
    description = fields.Text()
    quantity = fields.Integer()
    sale_id = fields.Many2one('sale.order', required=True)
    order_line_id = fields.Many2one('sale.order.line', domain="[('order_id', '=', sale_id)]")
    price_unit = fields.Float()


    @api.onchange('product_id')
    def get_description(self):
        for rec in self:
            rec.description=rec.product_id.description_sale