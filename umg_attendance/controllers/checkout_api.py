from odoo import http, fields
from odoo.http import request
from odoo.exceptions import ValidationError
from ..utils.jwt_helper import authenticate_jwt
import json

class CheckOutAPI(http.Controller):
    def json_response(self, data):
        return request.make_response(
            json.dumps(data),
            headers=[
                ('Content-Type', 'application/json')
            ]
        )
    
    @http.route(
        '/api/checkout',
        type='http',
        auth='none',
        methods=['POST'],
        csrf=False
    )

    def check_out(self, **kwargs):
        authorization = authenticate_jwt()
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
        
        today = fields.Date.today()
        # Find today's attendance
        attendance = request.env['attendance'].sudo().search([
            ('name', '=', employee.id),
            ('date', '=', today)
        ], limit=1)

        if not attendance:
            return self.json_response({
                'status' : False,
                'message' : 'You have not chcek in today!'
            })
        
        try:
            # Update check out time
            attendance.sudo().write({
                'check_out' : fields.Datetime.now(),
            })
            return self.json_response({
                'status' : True,
                'message' : 'Check out successful!',
                'attendance_id' : attendance.id,
                'name' : employee.name,
                'employee_code' : employee.employee_code,
                'date' : str(attendance.date) if attendance.date else "",'bu_name': employee.bu_name.name if employee.bu_name else "",
                'department': employee.department.name if employee.department else "",
                'check_in' : str(attendance.check_in) if attendance.check_in else "",
                'check_out' : str(attendance.check_out) if attendance.check_out else "",
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