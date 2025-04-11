from odoo import models,fields

class PathalogyGroups(models.Model):

    _name = "pathalogy.groups"
    _description = "This model stores the pathalogy group data in diseases"

    name = fields.Char(string="Name",required=True)
    code = fields.Char(default=lambda self: ('New'), readonly=True,string="Code")
    short_description = fields.Char(string="Short Description")

    def create(self, vals_list):
        """Automatically generate a sequence number for pathalogy groups."""
        vals_list['code'] = self.env['ir.sequence'].next_by_code('pathalogy.groups')
        return super(PathalogyGroups, self).create(vals_list)

class Diseases(models.Model):

    _name = "diseases.diseases"
    _description = 'Diseases Model to store the diseases data'

    name = fields.Char(string="Name",required=True)
    code = fields.Char(default=lambda self: ('New'),readonly=True,string="Code")
    diseases_category = fields.Selection([
        ('illness','Viral Illness'),
        ('injury','Injury')
    ],string="Diseases Category")

    def create(self, vals):
        """Automatically generate a sequence number for diseases."""
        vals['code'] = self.env['ir.sequence'].next_by_code('diseases.diseases')
        return super(Diseases, self).create(vals)
