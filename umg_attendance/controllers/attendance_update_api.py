from odoo import http, fields
from odoo.http import request
from ..utils.jwt_helper import authenticate_jwt
import json
from urllib.parse import parse_qs
from odoo.exceptions import ValidationError
from datetime import datetime

class AttendanceUpdateAPI(http.Controller):

    def json_response(self, data):
        return request.make_response(
            json.dumps(data),
            headers=[
                ('Content-Type', 'application/json')
            ]
        )
    
    @staticmethod
    def convert_datetime_format(value):

        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%d-%m-%Y %H:%M:%S",
            "%m-%d-%Y %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M:%S",
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(value, fmt)
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue

        raise ValueError(
            "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"
        )
    
    @http.route(
        '/api/attendance/update',
        type='http',
        auth='none',
        methods=['PATCH'],
        csrf=False
    )

    def attendance_update(self, **kwargs):
        authorization = authenticate_jwt()
        if isinstance(authorization, dict) and authorization.get('status') == False:
            return self.json_response(authorization)
        
        user_id = authorization.get('uid')
        if not user_id:
            return self.json_response({
                "status": False,
                "message": "User ID missing in token."
            })
        
        request.uid = user_id

        params = request.httprequest.form.to_dict()  
        attendance_id = int(params.get('attendance_id', 0))
        print("Attendance ID:", attendance_id, type(attendance_id))
        check_in = params.get('check_in', '')
        check_out = params.get('check_out', '')

        if not attendance_id:
            return self.json_response({
                'status' : False,
                'message' : 'Attendance ID is required!'
            })
        
        attendance = request.env['attendance'].browse(attendance_id)
        print("Attendance:", attendance)
        print("Exists:", attendance.exists())

        if not attendance.exists():
            return self.json_response({
                'status' : False,
                'message' : 'Attendance record not found!'
            })
        
        values = {}

        if check_in:
            values['check_in'] = self.convert_datetime_format(check_in)

        if check_out:
            values['check_out'] = self.convert_datetime_format(check_out)
        
        if not values:
            return self.json_response({
                'status': False,
                'message': 'No update values provided!'
            })

        attendance.write(values)

        return self.json_response({
            'status' : True,
            'message' : 'Attendance update successful!',
            'attendance_id' : attendance.id,
            'name' : attendance.name.name if attendance.name else "",
            'employee_code' : attendance.employee_code,
            'bu_name' : attendance.bu_name.name if attendance.bu_name else "",
            'department' : attendance.department.name if attendance.department else "",
            'check_in' : str(attendance.check_in) if attendance.check_in else "",
            'check_out' : str(attendance.check_out) if attendance.check_out else "",
            'status_value' : attendance.status,
        })