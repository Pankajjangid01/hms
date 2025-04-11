from odoo import models,fields,api


class RecreationalDrugs(models.Model):

    _name = "recreational.drugs"
    _description = "Creates the drugs information"

    name = fields.Char(string="Name",required=True)
    category = fields.Char(string="Category")
    toxicity = fields.Selection([
        ('high','High'),
        ('low','Low'),
        ('none','none')
    ],string="Toxicity")
    dependence = fields.Selection([
        ('high','High'),
        ('low','Low'),
        ('none','none')
    ],string="Dependence")
    street_names = fields.Char(readonly=True, copy=False,string="Street Names")

    @api.model
    def create(self, vals):
        """Automatically generate a street number for new drug."""
        vals['street_names'] = self.env['ir.sequence'].next_by_code('recreational.drugs')
        return super(RecreationalDrugs, self).create(vals)
