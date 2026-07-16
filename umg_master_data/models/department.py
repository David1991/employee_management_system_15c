from odoo import models,fields,api

class Department(models.Model):
    _name = "department"
    _description = "Department"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # For Department
    name = fields.Char(string="Department Name", required = True)
    code = fields.Char(string="Department Code", required = True)
    holding_business = fields.Many2one("business.unit", string="Holding Business", required = True)
    