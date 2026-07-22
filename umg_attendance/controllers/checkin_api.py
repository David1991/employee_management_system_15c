from odoo import http, fields
from odoo.http import request
from odoo.exceptions import ValidationError
from datetime import time
from ..utils.jwt_helper import authenticate_jwt
import json

class CheckInAPI(http.Controller):

    def json_response(self, data):
        return request.make_response(
            json.dumps(data),
            headers=[
                ('Content-Type', 'application/json')
            ]
        )
    @http.route(
        '/api/checkin',
        type='http',
        auth='none',
        methods=['POST'],
        csrf=False
    )

    def checkin(self, **kwargs):
        authorization = authenticate_jwt()

        print("========================")
        print("AUTHORIZATION:", authorization)
        print("TYPE:", type(authorization))
        print("========================")

        if isinstance(authorization, dict) and authorization.get('status') == False:
            return self.json_response(authorization)
        
        uid = authorization.get('uid')
        # Find employee linked with current user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', uid)
        ], limit=1)

        if not employee:
            return self.json_response({
                'status' : False,
                'message' : 'Employee not found!'
            })
        
        today = fields.Date.context_today(request.env.user)

        leave = request.env['leave'].sudo().search([
            ('name', '=', employee.id),
            ('status', '=', 'approve'),
            ('date_from', '<=', today),
            ('date_to', '>=', today),
        ], limit=1)

        if leave:
            return self.json_response({
                'status': False,
                'message': 'You are on approved leave today.'
            })
        
        # Check whether employee already checked in today
        attendance = request.env['attendance'].sudo().search([
            ('name', '=', employee.id),
            ('date', '=', today)
        ], limit=1)

        if attendance:
            return self.json_response({
                "status": False,
                "message": "You have already checked in today."
            })
        
        try:
            check_in = fields.Datetime.now()
            attendance_model = request.env['attendance']
            status = attendance_model.get_attendance_status(check_in)

            attendance = attendance_model.sudo().with_context(from_api = True).create({
                'name' : employee.id,
                'date' : today,
                'check_in' : check_in,
                'status' : status,
            })
            return self.json_response({
                'status' : True,
                'message' : 'Check In Successful!',
                'attendance_id' : attendance.id,
                'name' : employee.name,
                'employee_code' : employee.employee_code,
                'date' : str(attendance.date) if attendance.date else "",
                'bu_name' : employee.bu_name.name if employee.bu_name else "",
                'department' : employee.department.name if employee.department else "",
                'check_in' : str(attendance.check_in) if attendance.check_in else "",
                'status_value' : attendance.status,
            })
        except ValidationError as e:
            return self.json_response({
                'status' : False,
                'message' : str(e)
            })
        except Exception as e:
            return self.json_response({
                'status' : False,
                'message' : str(e)
            })