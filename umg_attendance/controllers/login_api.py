from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied
import json
import secrets

class LoginAPI(http.Controller):
    @http.route(
        '/api/login',
        type='json',
        auth='none',
        methods=['POST'],
        csrf=False
    )

    def login(self, **kwargs):
        db = kwargs.get('db')
        login = kwargs.get('login')
        password = kwargs.get('password')

        if not db or not login or not password:
            return {
                "status": False,
                "message": "Database, login and password are required."
            }
        
        try:
            # Authenticate User
            uid = request.session.authenticate(
                db,
                login,
                password
            )
        except AccessDenied:
            return {
                'status' : False,
                'message' : 'Invalid Username or Password!'
            }
        
        if not uid:
            return {
                'status' : False,
                'message' : 'Login Failed!'
            }
        # Get User Information
        user = request.env['res.users'].sudo().browse(uid)
        # Generate API Token
        token = secrets.token_hex(32)
        # Save Token
        user.write({
            'api_token' : token
        })
        # Find Employee linked to this user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', uid)
        ], limit=1)

        employee_data = {}
        if employee:
            employee_data = {
                'employee_id' : employee.id if employee else False,
                'employee_name' : employee.name if employee else "",
                'employee_code' : employee.employee_code if employee else "",
            }


        return {
            'status' : True,
            'message' : 'Login Successful!',
            'user_id' : user.id,
            'user_name' : user.name,
            'token' : token,
            'employee' : employee_data
        }