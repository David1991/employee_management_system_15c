import io
import base64
import xlsxwriter
from odoo import models, fields

class LeaveExcelReport(models.TransientModel):
    _name = "leave.excel.report"
    _description = "Leave Excel Report"

    file_name = fields.Char(string="File Name")
    file = fields.Binary(string="Excel File")

    def generate_excel(self, records):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet("Leave Report")

        # Header Style
        header_format = workbook.add_format({
            "bold": True,
            "align": "center",
        })

        headers = [
            "Employee Name",
            "Employee ID",
            "Employee Status",
            "BU Name",
            "Department",
            "Leave Title",
            "Entitled Days",
            "Taken Days",
            "Balance Days",
        ]

        row = 0
        for col, header in enumerate(headers):
            sheet.write(row, col, header, header_format)

        row += 1

        for leave in records:
            sheet.write(row, 0, leave["employee"])
            sheet.write(row, 1, leave["employee_code"])
            sheet.write(row, 2, leave["employee_status"])
            sheet.write(row, 3, leave["bu_name"])
            sheet.write(row, 4, leave["department"])
            sheet.write(row, 5, leave["leave_type"])
            sheet.write(row, 6, leave["entitled_days"])
            sheet.write(row, 7, leave["taken_days"])
            sheet.write(row, 8, leave["balance_days"])

            row += 1

        workbook.close()

        output.seek(0)

        file_data = base64.b64encode(output.read())

        self.write({
            "file": file_data,
            "file_name": "leave_report.xlsx"
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=leave.excel.report&id=%s&field=file&filename_field=file_name&download=true' % self.id,
            'target': 'self',
        }