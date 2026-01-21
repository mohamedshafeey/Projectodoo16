# -*- coding: utf-8 -*-
# from odoo import http


# class JournalTypeRef(http.Controller):
#     @http.route('/journal_type_ref/journal_type_ref', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/journal_type_ref/journal_type_ref/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('journal_type_ref.listing', {
#             'root': '/journal_type_ref/journal_type_ref',
#             'objects': http.request.env['journal_type_ref.journal_type_ref'].search([]),
#         })

#     @http.route('/journal_type_ref/journal_type_ref/objects/<model("journal_type_ref.journal_type_ref"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('journal_type_ref.object', {
#             'object': obj
#         })
