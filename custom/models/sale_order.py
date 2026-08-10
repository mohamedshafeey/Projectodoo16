# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date = fields.Date(string='Date')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')


