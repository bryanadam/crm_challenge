# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request

class ThemeCommon(http.Controller):

	@http.route('/client-application', type='http', auth="public", website=True)
	def country_search(self, **kw):
		country_rec = request.env['res.country'].sudo().browse(176)
		state_rec = []
		if country_rec:
			state_rec = request.env['res.country.state'].sudo().search([('country_id','=',country_rec.id)])

		glevel_rec = request.env['product.product'].sudo().search([])

		this = http.request.render(	'hr_crm.client_application', {
			'country_val'	: country_rec,
			'state_val'		: state_rec,
			'glevel_val'	: glevel_rec
			}
		)
		return this

	@http.route('/submit/client_application', type='http', auth="public", methods=['POST'], website=True)
	def client_application(self, **kw):
		partner = request.env['res.partner']
		name = "%s, %s" % (kw['stud_lname'] if 'stud_lname' in kw else '', kw['stud_fname'] if 'stud_fname' in kw else '')

		if kw['gender'] == 'Male':
			gender = 'm'
		elif kw['gender'] == 'Female':
			gender = 'f'
		else:
			gender = ''

		partner_value = {
			'name'			: name,
			'gender'		: gender,
			'company_type'	: 'person',
			'first_name'	: kw['stud_fname'] if 'stud_fname' in kw else '',
			'last_name'		: kw['stud_lname'] if 'stud_lname' in kw else '',
			'email'			: kw['email'] if 'email' in kw else '',
			'mobile'		: kw['phone'] if 'phone' in kw else '',
			'street'		: kw['street1'] if 'street1' in kw else '',
			'street2'		: kw['street2'] if 'street2' in kw else '',
			'city'			: kw['city'] if 'city' in kw else '',
			'country_id'	: int(kw['country_id']),
			'state_id'		: int(kw['state_id']),
			'zip'			: kw['zip'] if 'zip' in kw else ''
		}

		partner_id = partner.sudo().search([('first_name','=',kw['stud_fname']),('last_name','=',kw['stud_lname'])])
		if not partner_id:
			partner_id = partner.sudo().create(partner_value)

		product = request.env['product.product'].sudo().browse(int(kw['glevel_id']))
		states = request.env['res.country.state'].sudo().browse(int(kw['state_id']))

		crm_name = "%s - %s" % (name, product.name)

		crm_value = {
			'name'			: crm_name,
			'partner_id'	: partner_id.id,
			'team_id'		: states.team_id.id,
			'user_id'		: states.team_id.alias_user_id.id,
			'product_id'	: product.id,
			'description'	: kw['description'] if 'description' in kw else '',
		}

		request.env['crm.lead'].sudo().create(crm_value)

		return request.redirect('/contactus-thank-you')

