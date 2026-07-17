from odoo import http
from odoo.http import request
import json

class AttendanceAPI(http.Controller):
    
    @http.route(
        '/api/attendance',
        type='json',
        auth='user',
        methods=['GET'],
        csrf=False
    )
    def get_attendance(self):
        attendance = request.env['attendance'].sudo().search([])
        result = []

        for rec in attendance:
            result.append({
                'id' : rec.id,
                'name' : rec.name.name if rec.name else "",
                'employee_code' : rec.employee_code,
                'date' : rec.date,
                'bu_name' : rec.bu_name.name if rec.bu_name else "",
                'department' : rec.department.name if rec.department else "",
                'check_in' : rec.check_in,
                'check_out' : rec.check_out,
                'status' : rec.status,
            })
        return result