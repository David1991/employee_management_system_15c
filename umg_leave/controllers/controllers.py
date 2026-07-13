# -*- coding: utf-8 -*-
# from odoo import http


# class UmgLeave(http.Controller):
#     @http.route('/umg_leave/umg_leave', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/umg_leave/umg_leave/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('umg_leave.listing', {
#             'root': '/umg_leave/umg_leave',
#             'objects': http.request.env['umg_leave.umg_leave'].search([]),
#         })

#     @http.route('/umg_leave/umg_leave/objects/<model("umg_leave.umg_leave"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('umg_leave.object', {
#             'object': obj
#         })
