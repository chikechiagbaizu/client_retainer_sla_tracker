from odoo import models, fields
from dateutil.relativedelta import relativedelta

class RenewRetainer(models.TransientModel):
    _name = 'renew.retainer'
    _description = 'Renew Retainer'

    retainer_id = fields.Many2one(comodel_name="client.retainer", string="Retainer", required=True)
    hours_used = fields.Float(string="Hours Used", related="retainer_id.hours_used", readonly=True)
    renewal_date = fields.Date(string="Renewal Date", related="retainer_id.renewal_date", readonly=True)

    def action_renew_retainer(self):
        self.ensure_one()

        retainer = self.retainer_id
        
        retainer.write({
            'hours_used': 0,
            'renewal_date': (
                retainer.renewal_date + relativedelta(months=1) if retainer.renewal_date
                else fields.Date.today() + relativedelta(months=1)
            )
        })

        return {
            'type': 'ir.actions.act_window_close'
        }