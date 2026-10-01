from odoo.tests.common import TransactionCase

class ValidateHoursUsed(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()    
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer'
        })
    
    def test_hours_below_threshold(self):
        record = self.env['client.retainer'].create({
            'partner_id': self.partner.id,
            'hours_used': 31,
            'monthly_hours_allowance': 40
        })

        self.assertEqual(record.state,'normal')

    def test_hours_reaches_threshold(self):
        record = self.env['client.retainer'].create({
            'partner_id': self.partner.id,
            'hours_used': 32,
            'monthly_hours_allowance': 40
        })

        self.assertEqual(record.state,'warning')
    
    def test_hours_exceeds_allowance(self):
        record = self.env['client.retainer'].create({
            'partner_id': self.partner.id,
            'hours_used': 45,
            'monthly_hours_allowance': 40
        })

        self.assertEqual(record.state,'warning')