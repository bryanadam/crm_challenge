from odoo import api, fields, models, tools

class Crm_ResPartner(models.Model):
	_inherit = "res.partner"

	first_name = fields.Char(string="First Name")
	last_name = fields.Char(string="Last Name")
	gender = fields.Selection([('m','Male'),('f','Female')],string="Gender")