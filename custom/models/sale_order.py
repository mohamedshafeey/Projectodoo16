# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date = fields.Char(string='Date')
    datefrom = fields.Char(string='Date')

