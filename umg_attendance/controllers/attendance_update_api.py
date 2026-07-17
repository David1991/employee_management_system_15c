from odoo import http, fields
from odoo.http import request

class AttendanceUpdateAPI(http.Controller):
    @http.route(
        '/api/attendance/update',
        type='json',
        auth='user',
        methods=['POST'],
        csrf=False
    )

    def attendance_update(self, **kwargs):
        attendance_id = kwargs.get('attendance_id')
        check_in = kwargs.get('check_in')
        check_out = kwargs.get('check_out')

        if not attendance_id:
            return {
                'status' : False,
                'message' : 'Attendance ID is required!'
            }
        
        attendance = request.env['attendance'].sudo().browse(attendance_id)

        if not attendance.exists():
            return {
                'status' : False,
                'message' : 'Attendance record not found!'
            }
        
        values = {}

        if check_in:
            values['check_in'] = check_in

        if check_out:
            values['check_out'] = check_out

        attendance.sudo().write(values)

        return {
            'status' : True,
            'message' : 'Attendance update successful!',
            'attendance_id' : attendance.id,
            'name' : attendance.name.name,
            'employee_code' : attendance.name.employee_code,
            'bu_name' : attendance.name.bu_name.name,
            'department' : attendance.name.department.name,
            'check_in' : attendance.check_in,
            'check_out' : attendance.check_out,
            'status_value' : attendance.status,
        }