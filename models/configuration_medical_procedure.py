from odoo import models,fields

class MedicalProcedure(models.Model):

    _name = "medical.procedure"
    _description = "This Model stores the medical procedure"

    code = fields.Char(string="Code",required=True)
    long_text = fields.Char(string="Long Text",required=True)
