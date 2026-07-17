from odoo import http, fields
from odoo.http import request
from odoo.exceptions import ValidationError
from datetime import time

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

        leave = request.env['leave'].sudo().search([
            ('name', '=', employee.id),
            ('status', '=', 'approve'),
            ('date_from', '<=', today),
            ('date_to', '>=', today),
        ], limit=1)

        if leave:
            return {
                'status': False,
                'message': 'You are on approved leave today.'
            }
        
        # Check whether employee already checked in today
        attendance = request.env['attendance'].sudo().search([
            ('name', '=', employee.id),
            ('date', '=', today)
        ], limit=1)

        if attendance:
            return {
                "status": False,
                "message": "You have already checked in today."
            }
        
        try:
            check_in = fields.Datetime.now()

            # Calculate status
            # local_time = fields.Datetime.context_timestamp(
            #     request.env['attendance'],
            #     check_in
            # ).time()

            # if local_time <= time(8, 0):
            #     status = "present"

            # elif local_time <= time(9, 0):
            #     status = "late"

            # else:
            #     status = "absent"
            attendance_model = request.env['attendance']
            status = attendance_model.get_attendance_status(check_in)

            attendance = attendance_model.sudo().create({
                'name' : employee.id,
                # 'employee_code' : employee.employee_code,
                # 'bu_name' : employee.bu_name,
                # 'department' : employee.department,
                'date' : today,
                'check_in' : check_in,
                'status' : status,
            })
            return {
                'status' : True,
                'message' : 'Check In Successful!',
                'attendance_id' : attendance.id,
                'name' : employee.name,
                'employee_code' : employee.employee_code,
                'date' : attendance.date,
                'bu_name' : employee.bu_name,
                'department' : employee.department,
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