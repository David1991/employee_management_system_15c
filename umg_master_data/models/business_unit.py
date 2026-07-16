from odoo import models,fields,api

class BusinessUnit(models.Model):
    _name = "business.unit"
    _description = "Business Unit"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # For Business Unit
    name = fields.Char(string="Name", required = True)
    business_code = fields.Char(string="Business Code", required = True)
    business_type = fields.Char(string="Business Type", required = True)
    photo = fields.Image(string="Photo")
    