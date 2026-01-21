# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[('approval', 'Approval'), ('sale',)])
    project_name = fields.Many2one('sac.project', 'Project Name')
    project_ref = fields.Char('Project ref')
    sale_id = fields.Many2one('sale.order', string='Main Order')
    version_num = fields.Integer(default=1)
    alternative_order_ids = fields.One2many('alternative.order', 'sale_id')
    last_version = fields.Boolean(copy=fields)

    @api.constrains('last_version')
    def send_notfi_admin_sales(self):
        for rec in self:
            if rec.last_version:
                activity_obj = self.env['mail.activity'].sudo()
                activty_type = self.env.ref('mail.mail_activity_data_meeting')
                for user in self.env.ref('edit_so.group_last_version').users:
                    activity_obj.create(
                        {'summary': "{} please check : {}".format(user.name, rec.name),
                         'activity_type_id': activty_type.id,
                         'res_model_id': self.env.ref('sale.model_sale_order').id,
                         'res_id': rec.id,
                         'date_deadline': fields.Date.today(),
                         'user_id': user.id})

    def action_send_approval_payment(self):
        for rec in self:
            if not rec.last_version:
                raise UserError(_("The process cannot be completed except after the last version approval"))
            rec.state = 'approval'
            activity_obj = self.env['mail.activity'].sudo()
            activty_type = self.env.ref('mail.mail_activity_data_meeting')
            for user in self.env.ref('account.group_account_manager').users:
                activity_obj.create(
                    {'summary': "{} please confirm : {}".format(user.name, rec.name),
                     'activity_type_id': activty_type.id,
                     'res_model_id': self.env.ref('sale.model_sale_order').id,
                     'res_id': rec.id,
                     'date_deadline': fields.Date.today(),
                     'user_id': user.id})

    def action_edit_quantity(self):
        for rec in self:
            if rec.order_line:
                for line in rec.order_line:
                    line.write({
                        'product_uom_qty': line.qty_delivered,
                    })
                rec.picking_ids.filtered(lambda pick: pick.state not in ['done', 'cancel']).action_cancel()

    def copy_order(self):
        self.ensure_one()
        default = dict({}, name=f'{self.name}/{self.version_num}', sale_id=self.id)
        self.copy(default)
        self.version_num += 1

    def version_count(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Versions',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('sale_id', '=', self.id)],
        }

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
            activity_obj = self.env['mail.activity'].sudo()
            activty_type = self.env.ref('mail.mail_activity_data_meeting')
            for user in self.env.ref('edit_so.group_delivery_sale_order').users:
                for picking in rec.picking_ids:
                    activity_obj.create(
                        {'summary': "{} please check : {}".format(user.name, picking.name),
                         'activity_type_id': activty_type.id,
                         'res_model_id': self.env.ref('stock.model_stock_picking').id,
                         'res_id': picking.id,
                         'date_deadline': fields.Date.today(),
                         'user_id': user.id})
        return res

    def action_cancel(self):
        res = super().action_cancel()
        for rec in self:
            activity_obj = self.env['mail.activity'].sudo()
            activty_type = self.env.ref('mail.mail_activity_data_meeting')
            activity_obj.create(
                {'summary': "{} please check : {}".format(rec.user_id.name, rec.name),
                 'activity_type_id': activty_type.id,
                 'res_model_id': self.env.ref('sale.model_sale_order').id,
                 'res_id': rec.id,
                 'date_deadline': fields.Date.today(),
                 'user_id': rec.user_id.id})

        return res

