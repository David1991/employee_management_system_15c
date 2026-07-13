from odoo import models,fields,api
from datetime import date, time

class Attendance(models.Model):
    _name = "attendance"
    _description = "Attendance"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # For Attendance Form
    employee_name = fields.Many2one("hr.employee", string="Employee Name")
    employee_code = fields.Char(related = "employee_name.employee_code", string="Employee ID")
    date = fields.Date(string="Date", default = fields.Date.today)
    bu_name = fields.Many2one(related = "employee_name.bu_name", string="BU Name")
    department = fields.Many2one(related = "employee_name.department", string="Department")
    check_in = fields.Datetime(string="Check In")
    check_out = fields.Datetime(string="Check Out")
    status = fields.Selection([
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    ],string="Status", compute = "_compute_status", store = True)

    # The logic for status on base check_in time
    @api.depends('check_in')
    def _compute_status(self):
        for rec in self:
            rec.status = False

            if rec.check_in:
                check_in_time = fields.Datetime.context_timestamp(rec, rec.check_in).time()
                if check_in_time <= time(8, 0):
                    rec.status = "present"
                elif check_in_time <= time(9, 0):
                    rec.status = "late"
                else:
                    rec.status = "absent"
            # Odoo stores Datetime values in UTC in the database. "context_timestamp()" is converts the stored UTC time into the current user's local time before comparing it with user check in time.