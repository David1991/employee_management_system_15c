# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class umg_master_data(models.Model):
#     _name = 'umg_master_data.umg_master_data'
#     _description = 'umg_master_data.umg_master_data'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
