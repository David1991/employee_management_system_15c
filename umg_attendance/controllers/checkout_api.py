from odoo import http, fields
from odoo.http import request
from odoo.exceptions import ValidationError

class CheckOutAPI(http.Controller):
    @http.route(
        '/api/checkout',
        type='json',
        auth='user',
        methods=['POST'],
        csrf=False
    )

    def check_out(self, **kwargs):
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
        # Find today's attendance
        attendance = request.env['attendance'].sudo().search([
            ('name', '=', employee.id),
            ('date', '=', today)
        ], limit=1)

        if not attendance:
            return {
                'status' : False,
                'message' : 'You have not chcek in today!'
            }
        
        try:
            # Update check out time
            attendance.sudo().write({
                'check_out' : fields.Datetime.now(),
            })
            return {
                'status' : True,
                'message' : 'Check out successful!',
                'attendance_id' : attendance.id,
                'name' : employee.name,
                'employee_code' : employee.employee_code,
                'date' : attendance.date,
                'check_in' : attendance.check_in,
                'check_out' : attendance.check_out,
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