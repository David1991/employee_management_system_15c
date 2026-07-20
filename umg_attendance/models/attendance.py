from odoo import models,fields,api, _
from datetime import date, time
from odoo.exceptions import ValidationError

class Attendance(models.Model):
    _name = "attendance"
    _description = "Attendance"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # For Attendance Form
    name = fields.Many2one("hr.employee", string="Employee Name")
    employee_code = fields.Char(related = "name.employee_code", string="Employee ID")
    date = fields.Date(string="Date", default = fields.Date.context_today)
    bu_name = fields.Many2one(related = "name.bu_name", string="BU Name")
    department = fields.Many2one(related = "name.department", string="Department")
    check_in = fields.Datetime(string="Check In", default = fields.Datetime.now)
    check_out = fields.Datetime(string="Check Out")
    status = fields.Selection([
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    ],string="Status", tracking = True)

    # Check the condition of Manager and User for check in time
    @api.constrains("check_in")
    def _check_check_in_datetime(self):
        now = fields.Datetime.now()

        for rec in self:
            if not rec.check_in:
                continue

            # Attendance Manager can enter past check-in times
            if self.env.user.has_group("umg_attendance.group_attendance_manager"):
                continue

            # Attendance User cannot enter a past check-in time
            if rec.check_in < now:
                raise ValidationError(
                    _("Attendance users cannot enter a past check-in time.")
                )

    def write(self, vals):
        print("WRITE METHOD CALLED:", vals)
        if vals.get("check_in"):
            check_in = fields.Datetime.to_datetime(vals["check_in"])
            # vals.update({
            #     "status": self.get_attendance_status(check_in)
            # })

            vals["status"] = self.get_attendance_status(check_in)
            print("CHECK IN:", check_in)

        return super().write(vals)
    
    # The logic for status on base check_in time
    def get_attendance_status(self, check_in):

        check_in_time = fields.Datetime.context_timestamp(self.env.user, check_in).time()
        print("LOCAL CHECK IN TIME:", check_in_time)
        if check_in_time <= time(8, 0):
            return "present"
        elif check_in_time <= time(9, 0):
            return "late"
        else:
            return "absent"
        
    def auto_generate_absent(self):
        today = fields.Date.context_today(self)

        employees = self.env['hr.employee'].sudo().search([
            ('active', '=', True)
        ])

        Leave = self.env['leave']

        for employee in employees:
            attendance = self.search([
                ('name', '=', employee.id),
                ('date', '=', today)
            ], limit=1)

            if attendance:
                continue

            leave = Leave.search([
                ('name', '=', employee.id),
                ('status', '=', 'approve'),
                ('date_from', '<=', today),
                ('date_to', '>=', today),
            ], limit=1)

            if leave:
                continue

            self.create({
                'name' : employee.id,
                'date' : today,
                'status' : 'absent',
            })
            
    