from odoo import api, fields, models, tools

class Crm_CalendarEvent(models.Model):
	_inherit = "calendar.event"

	@api.model
	def create(self, values):
		meeting = super(Crm_CalendarEvent, self).create(values)
		if meeting.res_model == 'crm.lead':
			crm = self.env['crm.lead'].browse(meeting.res_id)
			stage = self.env['crm.stage'].search([('name','=','Meeting')])
			crm.update({'stage_id':stage.id}) # UPDATE CRM LEAD STAGE STATUS TO MEETING

		return meeting
