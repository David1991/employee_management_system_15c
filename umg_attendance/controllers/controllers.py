# -*- coding: utf-8 -*-
# from odoo import http


# class UmgAttendance(http.Controller):
#     @http.route('/umg_attendance/umg_attendance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/umg_attendance/umg_attendance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('umg_attendance.listing', {
#             'root': '/umg_attendance/umg_attendance',
#             'objects': http.request.env['umg_attendance.umg_attendance'].search([]),
#         })

#     @http.route('/umg_attendance/umg_attendance/objects/<model("umg_attendance.umg_attendance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('umg_attendance.object', {
#             'object': obj
#         })
