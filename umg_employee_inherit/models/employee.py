from odoo import models,fields,api
from datetime import date

class Employee(models.Model):
    _inherit = "hr.employee"
    _description = "Employee"
    
    # For Employee Form
    employee_code = fields.Char(string="Employee ID", readonly = "1")
    join_date = fields.Date(string="Join Date", required = True)
    phone_number = fields.Char(string="Phone Number")
    bu_name = fields.Many2one("business.unit", string="BU Name", required = True)
    department = fields.Many2one("department", string="Department", required = True)
    # department_name = fields.Many2one("department.department_name", string="Department Name")
    report_to = fields.Many2one("hr.employee", string="Report To")
    city_id = fields.Many2one("employee.city",string="City")
    township_id = fields.Many2one("employee.township",string="Township")
    street_id = fields.Many2one("employee.street",string="Street")
    home_no_id = fields.Many2one("employee.home.number",string="Home Number")
    status = fields.Selection([
        ('probation', 'Probation'),
        ('confirmation', 'Confirmation'),
    ],string="Status", default = "probation")
    active = fields.Boolean(string="Active", default = True)
    # For Attendance Form
    # date = fields.Date(string="Date")
    # check_in = fields.Datetime(string="Check In")
    # check_out = fields.Datetime(string="Check Out")
    # attendance_status = fields.Char(string="Attendance Status")
    # For Leave Form
    # date_from = fields.Date(string="Date From")
    # date_to = fields.Date(string="Date To")
    # duration = fields.Integer(string="Duration")
    # leave_type = fields.Char(string="Leave Type")
    # reason = fields.Text(string="Reason")
    # leave_status = fields.Char(string="Leave Status")

    @api.model
    def create(self, vals):
        vals['employee_code'] = self.env['ir.sequence'].next_by_code('hr.employee')
        return super(Employee, self).create(vals)

# For Employee City
class EmployeeCity(models.Model):
    _name = "employee.city"
    _description = "City"

    name = fields.Char(string="City", required=True)

# For Employee Township
class EmployeeTownship(models.Model):
    _name = "employee.township"
    _description = "Township"

    name = fields.Char(string="Township", required=True)
    # city_id = fields.Many2one("employee.city", string="City", required=True)

# For Employee Street
class EmployeeStreet(models.Model):
    _name = "employee.street"
    _description = "Street"

    name = fields.Char(string="Street", required=True)
    # township_id = fields.Many2one("employee.township", string="Township", required=True)

# For Employee Home Number
class EmloyeeHomeNumber(models.Model):
    _name = "employee.home.number"
    _description = "Home Number"

    name = fields.Char(string="Home Number", required=True)