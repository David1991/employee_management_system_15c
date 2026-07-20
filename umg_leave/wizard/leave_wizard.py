from odoo import models,fields, api
from datetime import date

class LeaveWizard(models.TransientModel):
    _name = "leave.wizard"
    _description = "wizard view for leave"

    # For Leave Form
    name = fields.Many2one("hr.employee", string="Employee Name")
    bu_name = fields.Many2one("business.unit", string="BU Name")
    department = fields.Many2one("department", string="Department")
    date_from = fields.Date(string="Date From", required = True)
    date_to = fields.Date(string="Date To", required = True)
    all_employee = fields.Boolean(string="All BU", default=True)
    
    # For Excel Report
    def action_print_excel(self):
        employees = self.env['hr.employee'].sudo().search([
            ('active', '=', True)
        ])

        domain = []

        # If All Employees is not checked, apply filters
        if not self.all_employee:
            if self.department:
                domain.append(("department", "=", self.department.id))
            if self.bu_name:
                domain.append(("bu_name", "=", self.bu_name.id))
            if self.name:
                domain.append(("id", "=", self.name.id))

        employees = self.env["hr.employee"].sudo().search(domain)

        data = []
        for employee in employees:

            leave_types = self.env['leave.type'].sudo().search([
                ('employee_status', '=', employee.status)
            ])
        
            for leave_type in leave_types:
                balance = self.env['leave'].get_leave_balance(employee, leave_type, fields.Date.today().year)

                data.append({
                    "employee" : employee.name or "",
                    "employee_code": employee.employee_code or "",
                    "employee_status": employee.status or "",
                    "bu_name": employee.bu_name.name if employee.bu_name else "",
                    "department": employee.department.name if employee.department else "",
                    "leave_type" : leave_type.name,
                    "entitled_days" : balance['entitled_days'],
                    "taken_days" : balance['taken_days'],
                    "balance_days" : balance['balance_days'],
                })

        report = self.env["leave.excel.report"].create({})

        return report.generate_excel(data)
