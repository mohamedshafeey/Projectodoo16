# -*- coding: utf-8 -*-

from odoo import models, fields, api


class account_move_line(models.Model):
    _inherit = 'account.move.line'

    amount_currency_float = fields.Float(compute="get_amount_currency_float", store=True, string="Amount Currency")
    standard_price = fields.Float(string="Cost", related="product_id.standard_price", store=True)
    mergen = fields.Float(compute="get_mergen", store=True)

    @api.depends('product_id', 'standard_price', 'price_unit')
    def get_mergen(self):
        for rec in self:
            rec.mergen = rec.price_unit - rec.standard_price

    @api.depends('amount_currency')
    def get_amount_currency_float(self):
        for rec in self:
            rec.amount_currency_float = rec.amount_currency


class account_move_line(models.Model):
    _inherit = 'account.move'

    mergen = fields.Float(compute="get_mergen", store=True)

    @api.depends('invoice_line_ids', 'invoice_line_ids.standard_price', 'invoice_line_ids.price_unit',
                 'invoice_line_ids.mergen')
    def get_mergen(self):
        for rec in self:
            rec.mergen = sum(rec.invoice_line_ids.mapped('mergen'))

    def ChangeCurrency(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Change Currency',
            'res_model': 'change.currency',
            'view_mode': 'form',
            'target': 'new',
        }


class ChangeCurrency(models.Model):
    _name = 'change.currency'

    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id, required=True)
    apply_manual_currency_exchange = fields.Boolean(string="", )
    manual_currency_exchange_rate_x = fields.Float(string='Manual Currency Exchange Rate',digits = (12,10))
    manual_currency_exchange_rate = fields.Float(string="", required=False,digits = (12,10) )

    @api.onchange('manual_currency_exchange_rate_x')
    def get_manual_currency_exchange_rate(self):
        for rec in self:
            if rec.manual_currency_exchange_rate_x:
                rec.manual_currency_exchange_rate = 1 /rec.manual_currency_exchange_rate_x
            else:
                rec.manual_currency_exchange_rate = 0

    def action_ok(self):
        for rec in self:
            invoice = self.env['account.move'].browse(self.env.context.get('active_ids'))
            for line in invoice.invoice_line_ids:
                if rec.apply_manual_currency_exchange:
                    line.price_unit = line.price_unit * rec.manual_currency_exchange_rate
                else:
                    line.price_unit = line.currency_id._convert(
                        line.price_unit,
                        rec.currency_id,
                        self.env.company,
                        fields.Date.context_today(self),
                    )
            invoice.update({
                'currency_id': rec.currency_id.id
            })


class account_Payment(models.Model):
    _inherit = 'account.payment'

    analytic_id = fields.Many2one(comodel_name="account.analytic.account")

    @api.constrains('analytic_id')
    def set_analytic_move(self):
        for rec in self:
            rec.move_id.line_ids.filtered(lambda l:l.balance > 0).update({'analytic_distribution': {rec.analytic_id.id: 100}})

    @api.model_create_multi
    def create(self, vals_list):
        res=super().create(vals_list)
        res.set_analytic_move()
        return res