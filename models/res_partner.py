from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    retainer_ids = fields.One2many(comodel_name='client.retainer', inverse_name='partner_id', string='Retainers')
    active_retainer_count = fields.Integer(compute='_compute_active_retainer_count', string='Active Retainer Count', store=True)

    @api.depends('retainer_ids.active')
    def _compute_active_retainer_count(self):
        for partner in self:
            partner.active_retainer_count = len(partner.retainer_ids.filtered(lambda r: r.active))