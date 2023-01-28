from odoo import api, fields, models, tools

class Crm_CrmLead(models.Model):
	_inherit = "crm.lead"

	product_id = fields.Many2one('product.product', string="Grade Level")
	vendor_id = fields.Many2one('res.partner', string="School", domain="[('supplier_rank','!=',0)]")

	def action_new_quotation(self):
		action = super(Crm_CrmLead, self).action_new_quotation()
		price = self.product_id.list_price
		if self.planned_revenue != 0:
			price = self.planned_revenue

		products = [{
			'product_id'		: self.product_id.id
		,	'name'				: self.product_id.name
		,	'product_uom'		: 1
		,	'product_uom_qty'	: 1
		,	'price_unit'		: price
		}]
		action['context'].update({'default_order_line': products})
		return action
