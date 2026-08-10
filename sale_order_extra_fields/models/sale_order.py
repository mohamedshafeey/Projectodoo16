# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    exta = fields.Char(string='Exta')
    extra_field_2 = fields.Char(string='Extra Field 2')
