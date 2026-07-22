from odoo import http
from odoo.http import request
import json
from ..utils.jwt_helper import authenticate_jwt

class AttendanceAPI(http.Controller):
    
    @http.route(
        '/api/attendance',
        type='http',
        auth='none',
        methods=['GET'],
        csrf=False
    )
    def get_attendance(self):

        authorization = authenticate_jwt()
        if isinstance(authorization, dict) and authorization.get('status') == False:
            return request.make_response(
                json.dumps(authorization),
                headers = [
                    ('Content-Type', 'application/json')
                ]
            )
        
        attendance = request.env['attendance'].sudo().search([])
        result = []

        for rec in attendance:
            result.append({
                'id' : rec.id,
                'name' : rec.name.name if rec.name else "",
                'employee_code' : rec.employee_code,
                'date' : str(rec.date) if rec.date else "",
                'bu_name' : rec.bu_name.name if rec.bu_name else "",
                'department' : rec.department.name if rec.department else "",
                'check_in' : str(rec.check_in) if rec.check_in else "",
                'check_out' : str(rec.check_out) if rec.check_out else "",
                'status' : rec.status,
            })
        return request.make_response(
            json.dumps(result),
            headers = [
                ('Content-Type', 'application/json')
            ]
        )