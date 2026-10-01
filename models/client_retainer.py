from odoo import models, fields, api

class ClientRetainer(models.Model):
    _name = 'client.retainer'
    _description = 'Client Retainer'

    _sql_constraints = [
        (
            'monthly_hours_allowance_constraints',
            'CHECK(monthly_hours_allowance > 0)',
            'monthly_hours_allowance should be greater than 0.'
        ),
        (
            'hours_used_constraints',
            'CHECK(hours_used >= 0)',
            'hours_used cannot be negative.'
        ),
    ]
    
    partner_id = fields.Many2one(comodel_name='res.partner', string='Client', required=True, ondelete='cascade')
    tier = fields.Selection(selection=[
        ('bronze','Bronze'),
        ('silver','Silver'),
        ('gold','Gold'),
    ], string="Tier", default="bronze")
    state = fields.Selection(selection=[
        ('normal','Normal'),
        ('warning','Warning'),
    ], string='State', compute='_compute_state', store=True)
    monthly_hours_allowance = fields.Float(string='Monthly Hours Allowance')
    hours_used = fields.Float(string='Hours Used')
    start_date = fields.Date(string='Start Date')
    renewal_date = fields.Date(string='Renewal Date')
    renewal_status = fields.Selection(selection=[
        ('success','Success'),
        ('failed','Failed')
    ], string='Renewal Status', compute='_compute_renewal_status', store=True)
    account_manager_id = fields.Many2one(comodel_name='res.users', string='Account Manager')
    active = fields.Boolean(string='Active', default=True)
    retainer_service_line_ids = fields.One2many(comodel_name='retainer.service.line', inverse_name='client_id', string='Retainer Service Line')
    
    @api.depends('hours_used','monthly_hours_allowance')
    def _compute_state(self):
        for record in self:
            warning_limit = record.monthly_hours_allowance * 0.80
            if record.hours_used >= warning_limit:
                record.state = 'warning'
            else:
                record.state = 'normal'

    @api.depends('start_date','renewal_date')
    def _compute_renewal_status(self):
        for record in self:
            if record.renewal_date and record.start_date and record.renewal_date <= record.start_date:
                record.renewal_status = 'failed'
            elif record.renewal_date and record.renewal_date <= fields.Date.today():
                record.renewal_status = 'failed'
            else:
                record.renewal_status = 'success'