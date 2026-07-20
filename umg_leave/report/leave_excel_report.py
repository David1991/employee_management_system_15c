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

        # Create formats
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter'
        })

        # Header Style
        header_format = workbook.add_format({
            "bold": True,
            "align": "center",
            "valign": "vcenter",
            "font_size": 12,
            "border": 1,
            "bg_color": '#D9EAD3',
            "text_wrap": True,
        })
        # For normal format
        normal_format = workbook.add_format({
            "font_size": 11,
            "border": 1,
            "valign": "vcenter",
        })
        # For number format
        number_format = workbook.add_format({
            "font_size": 11,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
        })

        # Column width
        sheet.set_column('A:A', 25)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 18)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 25)
        sheet.set_column('F:F', 25)
        sheet.set_column('G:G', 15)
        sheet.set_column('H:H', 15)
        sheet.set_column('I:I', 15)

        # Row height
        sheet.set_row(0, 30) #title
        sheet.set_row(1, 25) #header
        sheet.freeze_panes(2, 0)

        # Title
        sheet.merge_range(
            'A1:I1',
            'Leave Report',
            title_format
        )

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

        row = 2
        for col, header in enumerate(headers):
            sheet.write(row, col, header, header_format)

        row += 1

        for leave in records:
            sheet.write(row, 0, leave["employee"], normal_format)
            sheet.write(row, 1, leave["employee_code"], normal_format)
            sheet.write(row, 2, leave["employee_status"], normal_format)
            sheet.write(row, 3, leave["bu_name"], normal_format)
            sheet.write(row, 4, leave["department"], normal_format)
            sheet.write(row, 5, leave["leave_type"], normal_format)
            sheet.write(row, 6, leave["entitled_days"], number_format)
            sheet.write(row, 7, leave["taken_days"], number_format)
            sheet.write(row, 8, leave["balance_days"], number_format)

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