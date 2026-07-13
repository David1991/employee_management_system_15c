from odoo import models,fields, api
from datetime import date

class LeaveWizard(models.TransientModel):
    _name = "leave.wizard"
    _description = "wizard view for leave"

    # For Leave Form
    employee_name = fields.Many2one("hr.employee", string="Employee Name")
    bu_name = fields.Many2one("business.unit", string="BU Name")
    department = fields.Many2one("department", string="Department")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")

    # For excel report
    # def action_print_excel(self):
    #     leaves = self.env["leave"].search([
    #         ("employee_name", "=", self.employee_name.id)
    #     ])

    #     report = self.env["leave.excel.report"].create({})

    #     return report.generate_excel(leaves)
    
    # For Excel Report
    def action_print_excel(self):

        domain = []

        if self.department:
            domain.append(
                ("employee_name.department", "=", self.department.id)
            )

        if self.bu_name:
            domain.append(
                ("employee_name.bu_name", "=", self.bu_name.id)
            )

        if self.employee_name:
            domain.append(
                ("employee_name", "=", self.employee_name.id)
            )

        leaves = self.env["leave"].search(domain)

        report = self.env["leave.excel.report"].create({})

        return report.generate_excel(leaves)
