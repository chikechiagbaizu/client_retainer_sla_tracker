from odoo import fields
from odoo.tests.common import TransactionCase

class ValidateRenewalDate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer'
        })

    def test_renewal_date_less_than_start_date(self):
        record = self.env['client.retainer'].create({
            'partner_id': self.partner.id,
            'start_date': fields.Date.to_date('2026-04-01'),
            'renewal_date': fields.Date.to_date('2026-01-01'),
        })

        self.assertEqual(record.renewal_status, 'failed')

    def test_renewal_date_greater_than_start_date(self):
        record = self.env['client.retainer'].create({
            'partner_id': self.partner.id,
            'start_date': fields.Date.to_date('2026-04-01'),
            'renewal_date': fields.Date.to_date('2027-04-01')
        })

        self.assertEqual(record.renewal_status,'success')

    def test_renewal_date_future_date(self):
        record = self.env['client.retainer'].create({
            'partner_id': self.partner.id,
            'renewal_date': fields.Date.today()
        })

        self.assertEqual(record.renewal_status,'failed')