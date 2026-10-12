from odoo import models, fields, api, Command

class ClientRetainer(models.Model):
    _name = 'client.retainer'
    _description = 'Client Retainer'
    _inherit = ['renewable.subscription.mixin']

    _monthly_hours_allowance_constraints = models.Constraint(
        'CHECK(monthly_hours_allowance > 0)',
        'monthly_hours_allowance should be greater than 0.'
    )

    _hours_used_constraints = models.Constraint(
        'CHECK(monthly_hours_allowance > 0)',
        'monthly_hours_allowance should be greater than 0.'
    )
    
    partner_id = fields.Many2one(comodel_name='res.partner', string='Client', required=True, ondelete='cascade')
    tier = fields.Selection(selection=[
        ('bronze','Bronze'),
        ('silver','Silver'),
        ('gold','Gold'),
    ], string="Tier", default="bronze")
    monthly_value = fields.Float(compute="_compute_monthly_value", store=True, string='Monthly Value')
    
    state = fields.Selection(selection=[
        ('normal','Normal'),
        ('warning','Warning'),
    ], string='State', compute='_compute_state', store=True)
    monthly_hours_allowance = fields.Float(string='Monthly Hours Allowance')

    _TIER_PRICING = {
        'bronze': 500.0,
        'silver': 1200.0,
        'gold': 2500.0
    }

    hours_used = fields.Float(string='Hours Used')
    start_date = fields.Date(string='Start Date')
    renewal_status = fields.Selection(selection=[
        ('success','Success'),
        ('failed','Failed')
    ], string='Renewal Status', compute='_compute_renewal_status', store=True)
    account_manager_id = fields.Many2one(comodel_name='res.users', string='Account Manager')
    active = fields.Boolean(string='Active', default=True)
    retainer_service_line_ids = fields.One2many(
        comodel_name='retainer.service.line', 
        inverse_name='client_id', 
        string='Retainer Service Line'
        )
    last_invoiced_renewal = fields.Date(string='Last Invoiced Renewal', copy=False)

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
    
    @api.depends('tier')
    def _compute_monthly_value(self):
        for record in self:
            record.monthly_value = self._TIER_PRICING.get(record.tier, 0.0)

    @api.model
    def cron_renewal_date(self):
        deadline = fields.Date.add(fields.Date.today(), days=3)
        retainers = self.search([
            ('renewal_date','!=',False),
            ('renewal_date','<=',deadline)
        ])

        for record in retainers:
            if record.last_invoiced_renewal == record.renewal_date:
                continue
            self.env['account.move'].create({
                'partner_id': record.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name':f"Retainer Renewal ({record.tier}) - {record.partner_id.name}",
                        'quantity': 1.0,
                        'price_unit': record.monthly_value})
                        ]
                    })

            record.last_invoiced_renewal = record.renewal_date