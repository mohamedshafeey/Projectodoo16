from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'

    name = fields.Char(required=1, default="New", size=12)
    description = fields.Text()
    postcode = fields.Char(required=1)
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff= fields.Float(compute='_compute_diff')
    bedroom = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garage_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default='north')


    tag = fields.Many2many('tag')
    owner_id = fields.Many2one('owner')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'pending'),
        ('sold', 'Sold'),

    ], default='draft')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!')
    ]

    @api.depends('expected_price','selling_price')
    def _compute_diff(self):
        for rec in (self):
            print("inside _compute_diff method")
            rec.diff = rec.expected_price - rec.selling_price

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for record in self:
            if record.bedrooms == 0:
                raise ValidationError("Please add valid number of bedrooms!")

    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        print('inside create method')
        return res

    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     return super(Property, self)._search(
    #         domain, offset=offset, limit=limit, order=order,
    #         access_rights_uid=access_rights_uid
    #     )

    def write(self, vals):
        res = super(Property, self).write(vals)
        print('inside write method')
        return res

    def unlink(self):
        res = super(Property, self).unlink()
        print('inside unlink method')
        return res


    def action_draft(self):
        for rec in (self):
            print("inside draft action")
            rec.state = 'draft'


    def action_pending(self):
        for rec in (self):
            print("inside pending action")
            rec.state = 'pending'

    def action_sold(self):
        for rec in (self):
           print("inside sold action")
           rec.state = 'sold'