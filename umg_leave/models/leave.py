from odoo import models,fields,api, _
from datetime import date
from odoo.exceptions import ValidationError

class Leave(models.Model):
    _name = "leave"
    _description = "Leave"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # For Leave Form
    employee_name = fields.Many2one("hr.employee", string="Employee Name")
    employee_code = fields.Char(related = "employee_name.employee_code", string="Employee ID")
    bu_name = fields.Many2one(related = "employee_name.bu_name", string="BU Name")
    department = fields.Many2one(related = "employee_name.department", string="Department")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    duration = fields.Integer(string="Duration", compute = "_compute_duration", store = True)
    leave_title = fields.Many2one("leave.type", string="Leave Title")
    allocation_year = fields.Integer(string="Allocation Year",
        default=lambda self: fields.Date.today().year, required=True)
    entitled_days = fields.Integer(related="leave_title.entitled_days",
    string="Entitled Days", store=True)
    taken_days = fields.Integer(related="duration", store=True, string="Taken Days")
    balance_days = fields.Integer(compute="_compute_balance_days",
    string="Balance Days", store=True)
    report_to = fields.Many2one("hr.employee", string="Report To")
    reason = fields.Text(string="Reason")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ],string="Status", default = "draft")

    # Calculating for duration depend on date_from and date_to
    @api.depends("date_from", "date_to")
    def _compute_duration(self):
        for rec in self:
            rec.duration = 0

            if rec.date_from and rec.date_to:
                rec.duration = (rec.date_to - rec.date_from).days + 1

    # Check date for date_from and date_to
    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        today = fields.Date.today()

        for rec in self:
            if rec.date_from and rec.date_to:
                # Date To can't be before Date From
                if rec.date_to < rec.date_from:
                    raise ValidationError(
                        "Date To must be greater than Date From!"
                    )
                # Employees can't request leave before Today
                if rec.date_from < today:
                    raise ValidationError(
                        "You cannot apply leave for a past date!"
                    )
                
    # Calculating the leave balance days depend on employee name, leave type,allocation year and entitled days
    @api.depends("employee_name", "leave_title", "allocation_year", "entitled_days")
    def _compute_balance_days (self):
        Leave = self.env['leave']
        for rec in self:
             year_start = date(rec.allocation_year, 1, 1)
             year_end = date(rec.allocation_year, 12, 31)

             leaves = Leave.search([
                ("employee_name", "=", rec.employee_name.id),
                ("leave_title", "=", rec.leave_title.id),
                ("status", "=", "approve"),
                ("date_from", ">=", year_start),
                ("date_from", "<=", year_end),])

             taken_days = sum(leaves.mapped("duration"))

             rec.balance_days = rec.entitled_days - taken_days
