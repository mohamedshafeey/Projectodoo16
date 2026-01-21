from odoo import fields, models, api
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    alternative_order_ids = fields.One2many('alternative.order', 'order_line_id')
    price_unit_after_discount = fields.Float(readonly=True)

    @api.onchange('price_unit', 'discount')
    def get_price_unit_after_discount(self):
        for rec in self:
            rec.price_unit_after_discount = rec.price_unit - (rec.price_unit * rec.discount / 100)

    @api.onchange('discount')
    def check_discount(self):
        for rec in self:
            limit = int(self.env['ir.config_parameter'].sudo().get_param('edit_so.limit_discount'))
            manger_limit = int(self.env['ir.config_parameter'].sudo().get_param('edit_so.manger_limit_discount'))
            if self.env.user.id in self.env.ref('edit_so.group_unlimited_discount').users.ids:
                print()
            elif self.env.user.id in self.env.ref(
                    'sales_team.group_sale_manager').users.ids and rec.discount > manger_limit:
                raise UserError("Discount limit is %s" % manger_limit)
            elif self.env.user.id not in self.env.ref(
                    'sales_team.group_sale_manager').users.ids and rec.discount > limit:
                raise UserError("Discount limit is %s" % limit)



class ResConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    limit_discount = fields.Integer(string="Discount Limit", default=10, config_parameter='edit_so.limit_discount')
    manger_limit_discount = fields.Integer(string="Discount Manger Limit", default=20,
                                           config_parameter='edit_so.manger_limit_discount')
