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
    country_id = fields.Many2one("company.country",string="Country", required = True)
    city_id = fields.Many2one("company.city",string="City", required = True)
    township_id = fields.Many2one("company.township",string="Township", required = True)
    street_id = fields.Many2one("company.street",string="Street", required = True)
    home_no_id = fields.Many2one("company.home.number",string="Home Number", required = True)
    
    # For Company Country
class CompanyCountry(models.Model):
    _name = "company.country"
    _description = "Country"
    
    name = fields.Char(string="Country", required=True)
    
    # For Company City
class CompanyCity(models.Model):
    _name = "company.city"
    _description = "City"
    
    name = fields.Char(string="City", required=True)
    
    # For Company Township
class CompanyTownship(models.Model):
    _name = "company.township"
    _description = "Township"
    
    name = fields.Char(string="Township", required=True)
    
    # For Company Street
class CompanyStreet(models.Model):
    _name = "company.street"
    _description = "Street"
    
    name = fields.Char(string="Street", required=True)
    
    # For Company Home Number
class CompanyHomeNumber(models.Model):
    _name = "company.home.number"
    _description = "Home Number"
    
    name = fields.Char(string="Home Number", required=True)
    