# -*- coding: utf-8 -*-
# from odoo import http


# class UmgEmployeeInherit(http.Controller):
#     @http.route('/umg_employee_inherit/umg_employee_inherit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/umg_employee_inherit/umg_employee_inherit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('umg_employee_inherit.listing', {
#             'root': '/umg_employee_inherit/umg_employee_inherit',
#             'objects': http.request.env['umg_employee_inherit.umg_employee_inherit'].search([]),
#         })

#     @http.route('/umg_employee_inherit/umg_employee_inherit/objects/<model("umg_employee_inherit.umg_employee_inherit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('umg_employee_inherit.object', {
#             'object': obj
#         })
