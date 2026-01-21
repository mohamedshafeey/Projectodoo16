# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    journal_ref = fields.Char(copy=False)

    def _post(self, soft=True):
        for rec in self:
            if not rec.journal_ref and not rec.journal_id.default_sequence:
                if rec.journal_id.type == 'sale':
                    rec.name = self.env['ir.sequence'].next_by_code('journal.sale')
                elif rec.journal_id.type == 'purchase':
                    rec.name = self.env['ir.sequence'].next_by_code('journal.purchase')
                elif rec.journal_id.type == 'cash':
                    rec.name = self.env['ir.sequence'].next_by_code('journal.cash')
                elif rec.journal_id.type == 'bank':
                    rec.name = self.env['ir.sequence'].next_by_code('journal.bank')
                elif rec.journal_id.type == 'general':
                    rec.name = self.env['ir.sequence'].next_by_code('journal.general')
        return super()._post(soft=soft)

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    default_sequence = fields.Boolean()
