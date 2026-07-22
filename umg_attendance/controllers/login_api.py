from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied
import json
import jwt
from datetime import datetime, timedelta
from odoo.tools import config
from urllib.parse import parse_qs

JWT_SECRET = config.get('jwt_secret')
JWT_ALGORITHM = "HS256"

class LoginAPI(http.Controller):
    def json_response(self, data):
        return request.make_response(
            json.dumps(data),
            headers=[
                ('Content-Type', 'application/json')
            ]
        )
    @http.route(
        '/api/login',
        type='http',
        auth='none',
        methods=['POST'],
        csrf=False
    )

    def login(self, **kwargs):
        params = request.httprequest.form.to_dict()
        
        print("====================")
        print("METHOD:", request.httprequest.method)
        print("CONTENT TYPE:", request.httprequest.content_type) 
        print("PARAMS:", params)
        print("====================")

        db = params.get('db', '')
        login = params.get('login', '')
        password = params.get('password', '')

        if not db or not login or not password:
            return self.json_response({
                    "status": False,
                    "message": "Database, login and password are required."
                })
        
        try:
            # Authenticate User
            uid = request.session.authenticate(
                db,
                login,
                password
            )
        except AccessDenied:
            return self.json_response({
                'status' : False,
                'message' : 'Invalid Username or Password!'
            })
        
        if not uid:
            return self.json_response({
                'status' : False,
                'message' : 'Login Failed!'
            })
        # Get User Information
        user = request.env['res.users'].sudo().browse(uid)

        payload = {
            "uid" : user.id,
            "login" : user.login,
        }
        token = jwt.encode(
            payload,
            JWT_SECRET,
            algorithm = JWT_ALGORITHM
        )
        
        # Find Employee linked to this user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', uid)
        ], limit=1)

        employee_data = {}
        if employee:
            employee_data = {
                'employee_id' : employee.id if employee else False,
                'name' : employee.name if employee else "",
                'employee_code' : employee.employee_code if employee else "",
            }


        return self.json_response({
            'status' : True,
            'message' : 'Login Successful!',
            'user_id' : user.id,
            'user_name' : user.name,
            'token' : token,
            'employee' : employee_data
        })