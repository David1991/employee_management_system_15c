from odoo import models,fields,api, _
from datetime import date
from odoo.exceptions import ValidationError

class Leave(models.Model):
    _name = "leave"
    _description = "Leave"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # For Leave Form
    name = fields.Many2one("hr.employee", string="Employee Name")
    employee_code = fields.Char(related = "name.employee_code", string="Employee ID")
    employee_status = fields.Selection(related = "name.status", string = "Employee Status", store = True)
    bu_name = fields.Many2one(related = "name.bu_name", string="BU Name")
    department = fields.Many2one(related = "name.department", string="Department")
    date_from = fields.Date(string="Date From", required = True)
    date_to = fields.Date(string="Date To", required = True)
    duration = fields.Integer(string="Duration", compute = "_compute_duration", store = True)
    leave_title = fields.Many2one("leave.type", string="Leave Title", required = True)
    allocation_year = fields.Integer(string="Allocation Year",
        default=lambda self: fields.Date.today().year, required=True)
    # A lambda is an anonymous (unnamed) function.
    entitled_days = fields.Integer(compute="_compute_entitled_days",
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

    def action_approve(self):
        for rec in self:
            rec.status = "approve"

    def action_reject(self):
        for rec in self:
            rec.status = "reject"

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
                
                # Leave Manager can create backdated leave
                if not self.env.user.has_group("umg_leave.group_leave_manager"):
                    # Employees can't request leave before Today
                    if rec.date_from < today:
                        raise ValidationError(
                            "You cannot apply leave for a past date!"
                        )
                
    # Check the entitled days depend on leave title and employee status
    @api.depends("leave_title", "name", "name.status")
    def _compute_entitled_days(self):
        for rec in self:
            rec.entitled_days = 0

            if rec.leave_title and rec.employee_status:

                entitlement = self.env["leave.type"].search([
                    ("name", "=", rec.leave_title.name),
                    ("employee_status", "=", rec.employee_status),
                ], limit=1)

                if entitlement:
                    rec.entitled_days = entitlement.entitled_days 

    # Calculating the leave balance days depend on employee name, leave type,allocation year and entitled days
    @api.depends("name", "employee_status", "leave_title", "allocation_year", "entitled_days", "duration", "status")
    def _compute_balance_days (self):
        Leave = self.env['leave']
        # LeaveEntitlement = self.env["leave.entitlement"]

        for rec in self:     

             if not rec.name or not rec.leave_title:
                continue

             # Find entitlement based on leave type and employee status
            #  entitlement = LeaveEntitlement.search([
            #         ("leave_type_id", "=", rec.leave_title.id),
            #         ("employee_status", "=", rec.employee_status),
            #     ], limit=1)

            #  entitled_days = entitlement.entitled_days if entitlement else 0
    
             year_start = date(rec.allocation_year, 1, 1)
             year_end = date(rec.allocation_year, 12, 31)

             leaves = Leave.search([
                ("name", "=", rec.name.id),
                ("leave_title", "=", rec.leave_title.id),
                ("status", "=", "approve"),
                ("date_from", ">=", year_start),
                ("date_from", "<=", year_end),])

             taken_days = sum(leaves.mapped("duration"))

             rec.balance_days = rec.entitled_days - taken_days
    
    # UI shown Leave/John Doe/Casual Leave/2 Days/07-19-2026
    def name_get(self):
        result = []

        for rec in self:
            employee = rec.name.name if rec.name else ""
            leave_title = rec.leave_title.name if rec.leave_title else ""
            duration = rec.duration or 0
            date_from = ""
            if rec.date_from:
                date_from = rec.date_from.strftime("%m-%d-%y")

                display_name = f"{employee}/ {leave_title}/ {duration} Days/ {date_from}"

                result.append((rec.id, display_name))
        return result
    
    def get_leave_balance(self, name, leave_type, allocation_year):
        year_start = date(allocation_year, 1, 1)
        year_end = date(allocation_year, 12, 31)

        entitlement = self.env['leave.type'].sudo().search([
            ('name', '=', leave_type.name),
            ('employee_status', '=', name.status),
        ], limit=1)
        entitled_days = entitlement.entitled_days if entitlement else 0

        leaves = self.search([
            ('name', '=', name.id),
            ('leave_title', '=', leave_type.id),
            ('status', '=', 'approve'),
            ('date_from', '>=', year_start),
            ('date_from', '<=', year_end),
        ])

        taken_days = sum(leaves.mapped('duration'))

        return {
            "entitled_days": entitled_days,
            "taken_days": taken_days,
            "balance_days": entitled_days - taken_days,
        }
