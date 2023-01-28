from odoo import api, fields, models, tools

class Crm_ResCountryState(models.Model):
	_inherit = "res.country.state"

	team_id = fields.Many2one('crm.team', string="Sales Team")