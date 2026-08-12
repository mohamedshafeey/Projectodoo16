# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    younes = fields.Char(string='Younes')
    yahia = fields.Integer(string='Yahia')
