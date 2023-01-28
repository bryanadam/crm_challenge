from odoo import api, fields, models, tools
from datetime import datetime


class Crm_SaleOrder(models.Model):
	_inherit = "sale.order"

	def action_create_purchase(self):
		order_lines = []
		for lines in self.order_line:
			order_lines.append((0, 0, {
				'sale_line_id'	: lines.id,
				'sale_order_id'	: lines.order_id.id,
				'name'			: lines.name,
				'product_id'	: lines.product_id.id,
				'product_uom'	: lines.product_uom.id,
				'product_qty'	: lines.product_uom_qty,
				'price_unit'	: lines.price_unit,
				'taxes_id'		: [(6, 0, lines.tax_id.ids)],
				'date_planned'	: datetime.now()
			}))
		order = {
			'partner_id'	: self.opportunity_id.vendor_id.id,
			'origin'		: self.name,
			'date_order'	: datetime.now(),
			'order_line'	: order_lines,
			'sale_id'		: self.id,

		}
		purchase = self.env['purchase.order'].create(order)
		purchase.button_confirm()
		self._compute_purchase_order_count()

	@api.model_create_multi
	def create(self, vals_list):
		action = super(Crm_SaleOrder, self).create(vals_list)
		if action.opportunity_id:
			crm = self.env['crm.lead'].browse(action.opportunity_id.id)
			stage = self.env['crm.stage'].search([('name','=','Proposal')])
			crm.update({'stage_id':stage.id}) # UPDATE CRM LEAD STAGE STATUS TO PROPOSAL
		return action

	def action_confirm(self):
		action = super(Crm_SaleOrder, self).action_confirm()
		if self.opportunity_id:
			crm = self.opportunity_id
			stage = self.env['crm.stage'].search([('name','=','Negotiation and commitment')])
			crm.update({'stage_id':stage.id}) # UPDATE CRM LEAD STAGE STATUS TO NEGOTIATION AND COMMITMENT
		return action

class Crm_PurchaseOrder(models.Model):
	_inherit = "purchase.order"

	sale_id = fields.Many2one('sale.order')
