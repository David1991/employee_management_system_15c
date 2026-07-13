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
            sheet.write(row, 0, leave.employee_name.name)
            sheet.write(row, 1, leave.employee_code)
            sheet.write(row, 2, leave.bu_name.name)
            sheet.write(row, 3, leave.department.name)
            sheet.write(row, 4, leave.leave_title.name)
            sheet.write(row, 5, leave.entitled_days)
            sheet.write(row, 6, leave.duration)
            sheet.write(row, 7, leave.balance_days)

            row += 1

        workbook.close()

        output.seek(0)

        file_data = base64.b64encode(output.read())

        self.write({
            "file": file_data,
            "file_name": "leave_report.xlsx"
        })

        return {
            "type": "ir.actions.act_window",
            "res_model": "leave.excel.report",
            "view_mode": "form",
            "target": "new",
            "res_id": self.id,
        }