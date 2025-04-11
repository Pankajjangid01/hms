from odoo import models, fields

class TestingUnits(models.Model):

    _name = "testing.units"
    _description = "This model store the lab testing units"
    _rec_name = "name"

    name = fields.Selection([
        ('gream','Grams(g)'),
        ('milligrams','Milligrams(mg)'),
        ('mililiters','Mililiters(ml)')
    ],string="Name",required=True)
    code = fields.Selection([
        ('gream','Grams(g)'),
        ('milligrams','Milligrams(mg)'),
        ('mililiters','Mililiters(ml)')
    ],string="Code")

class TestType(models.Model):

    _name = "test.type"
    _description = "this model store the test type details"
    _rec_name = "name"

    test_code = fields.Char(string="Code",readonly=True)
    name = fields.Char(string="name",required=True)

    def create(self, vals):
        """Automatically generate a test sequence."""
        vals['test_code'] = self.env['ir.sequence'].next_by_code('test.type')
        return super(TestType, self).create(vals)
