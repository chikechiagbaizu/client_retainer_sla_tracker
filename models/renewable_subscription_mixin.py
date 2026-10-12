from odoo import models, fields, api

class RenewableSubscriptionMixin(models.AbstractModel):
    _name = 'renewable.subscription.mixin'
    _description = 'Renewable Subscription Mixin'

    renewal_date = fields.Date(string='Renewal Date')
    days_until_renewal = fields.Integer(
        string='Days Until Renewal', 
        compute='_compute_days_until_renewal')

    @api.depends('renewal_date')
    def _compute_days_until_renewal(self):
        today = fields.Date.today()
        
        for record in self:
            record.days_until_renewal = (
                (record.renewal_date - today).days if record.renewal_date
                else 0
            )