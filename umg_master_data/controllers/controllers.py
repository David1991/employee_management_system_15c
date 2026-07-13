# -*- coding: utf-8 -*-
# from odoo import http


# class UmgMasterData(http.Controller):
#     @http.route('/umg_master_data/umg_master_data', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/umg_master_data/umg_master_data/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('umg_master_data.listing', {
#             'root': '/umg_master_data/umg_master_data',
#             'objects': http.request.env['umg_master_data.umg_master_data'].search([]),
#         })

#     @http.route('/umg_master_data/umg_master_data/objects/<model("umg_master_data.umg_master_data"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('umg_master_data.object', {
#             'object': obj
#         })
