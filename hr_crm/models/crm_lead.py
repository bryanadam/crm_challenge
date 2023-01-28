from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError

class Crm_CrmLead(models.Model):
	_inherit = "crm.lead"

	product_id = fields.Many2one('product.product', string="Grade Level")
	vendor_id = fields.Many2one('res.partner', string="School", domain="[('supplier_rank','!=',0)]")

	purchase_order_count = fields.Integer("Number of Purchase Order", compute='_compute_purchase_order_count')


	def action_new_quotation(self):
		""" add order line when create sale order """
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

	def action_set_won_rainbowman(self):
		""" Create purchase order when status in Won """
		if not self.vendor_id:
			raise ValidationError(_("Please fill up Vendor"))
		sales = self.env['sale.order'].search([('opportunity_id','=',self.id)])

		for sale in sales:
			sale.action_create_purchase()

		action = super(Crm_CrmLead, self).action_set_won_rainbowman()
		return action

	def _compute_purchase_order_count(self):
		order = self.env['purchase.order'].search([('sale_id.opportunity_id','=',self.id)])
		for lead in self:
			lead.purchase_order_count = len(order)

	def action_view_purchase(self):
		action = self.env['ir.actions.act_window'].for_xml_id('purchase', 'purchase_rfq')
		action['domain'] = [('sale_id.opportunity_id','=',self.id)]
		action['target'] = 'current'
		return action


