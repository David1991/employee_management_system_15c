from odoo import models,fields,api

class LeaveType(models.Model):
    _name = "leave.type"
    _description = "Leave Type"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Leave Type", required = True)
    entitlement_ids = fields.One2many("leave.entitlement", "leave_type_id",
    string="Entitlements")