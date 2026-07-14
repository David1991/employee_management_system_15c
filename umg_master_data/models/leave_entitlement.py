from odoo import models, fields


class LeaveEntitlement(models.Model):
    _name = "leave.entitlement"
    _description = "Leave Entitlement"

    leave_type_id = fields.Many2one("leave.type", string="Leave Type",
    required=True, ondelete="cascade")
    employee_status = fields.Selection([
        ('probation', 'Probation'),
        ('confirmation', 'Confirmation'),
    ], string="Employee Status", required=True)
    entitled_days = fields.Integer(string="Entitled Days", required=True)