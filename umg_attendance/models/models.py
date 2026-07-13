# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class umg_attendance(models.Model):
#     _name = 'umg_attendance.umg_attendance'
#     _description = 'umg_attendance.umg_attendance'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
