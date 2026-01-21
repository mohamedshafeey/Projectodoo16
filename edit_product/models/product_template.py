# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductBrand(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Selection(default='product')
    invoice_policy = fields.Selection(default='delivery')
    tracking = fields.Selection(default='serial')
