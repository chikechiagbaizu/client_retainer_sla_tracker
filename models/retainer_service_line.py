from odoo import models, fields

class RetainerServiceLine(models.Model):
    _name = 'retainer.service.line'
    _description = 'Retainer Service Line'

    client_id = fields.Many2one(comodel_name='client.retainer', string='Client', ondelete='cascade')
    date = fields.Date(string='Date')
    description = fields.Text(string='Description')
    hours_logged = fields.Integer(string='Hours Logged')