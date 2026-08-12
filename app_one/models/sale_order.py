from odoo import models, fields


class SaleNoha(models.Model):
    _inherit = 'sale.order'

    property_id = fields.Many2one('property')


# def action_confirm(self):
#     res = super(SaleOrder, self).action_confirm(vals)
#     print('inside action_confirm method')
#     return res