from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    retainer_id = fields.Many2one(
        comodel_name='client.retainer',
        string='Client Retainer',
        domain="[('partner_id','=',partner_id)]"
        )