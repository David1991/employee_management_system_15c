# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeManagementSystem(http.Controller):
#     @http.route('/employee_management_system/employee_management_system', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_management_system/employee_management_system/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_management_system.listing', {
#             'root': '/employee_management_system/employee_management_system',
#             'objects': http.request.env['employee_management_system.employee_management_system'].search([]),
#         })

#     @http.route('/employee_management_system/employee_management_system/objects/<model("employee_management_system.employee_management_system"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_management_system.object', {
#             'object': obj
#         })
