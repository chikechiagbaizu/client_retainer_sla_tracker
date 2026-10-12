from odoo import models, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'product_uom_qty','order_id.retainer_id')
    def _onchange_retainer_tier_discount(self):
        discounts = {
            'bronze': 10,
            'silver': 15,
            'gold': 20
        }

        for line in self:
            retainer = line.order_id.retainer_id

            if retainer:
                line.discount = discounts.get(retainer.tier, 0)
            else:
                line.discount = 0