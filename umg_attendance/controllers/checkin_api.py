from odoo import http, fields
from odoo.http import request
from odoo.exceptions import ValidationError

class CheckInAPI(http.Controller):
    @http.route(
        '/api/checkin',
        type='json',
        auth='user',
        methods=['POST'],
        csrf=False
    )

    def checkin(self, **kwargs):
        # Find employee linked with current user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)

        if not employee:
            return {
                'status' : False,
                'message' : 'Employee not found!'
            }
        
        today = fields.Date.context_today(request.env.user)
        # Check whether employee already checked in today
        attendance = request.env['attendance'].sudo().search([
            ('employee_name', '=', employee.id),
            ('date', '=', today)
        ], limit=1)

        if attendance:
            return {
                "status": False,
                "message": "You have already checked in today."
            }
        
        try:
            attendance = request.env['attendance'].sudo().create({
                'employee_name' : employee.id,
                'date' : today,
                'check_in' : fields.Datetime.now(),
            })
            return {
                'status' : True,
                'message' : 'Check In Successful!',
                'attendance_id' : attendance.id,
                'employee_name' : employee.name,
                'employee_code' : employee.employee_code,
                'date' : attendance.date,
                'check_in' : attendance.check_in,
                'status_value' : attendance.status,
            }
        except ValidationError as e:
            return {
                'status' : False,
                'message' : str(e)
            }
        except Exception as e:
            return {
                'status' : False,
                'message' : str(e)
            }