import re
from odoo import models,fields,api
from odoo.exceptions import ValidationError


class Genetics(models.Model):

    _name = "genetics.genetics"
    _description = "store the genetics data"

    name = fields.Char(string="Name",required=True)
    official_long_name = fields.Char(string="Official Long Name")
    affected_chromosome = fields.Char(string="Affected Chromosome")
    dominance = fields.Char(string="Dominance")
    location = fields.Char(string="Location")
    information = fields.Char(string="Information")

    @api.constrains('name')
    def check_patient_name(self):
        """Method to validate the name of the patient"""
        if self.name and not re.fullmatch(r"^[A-Za-z ]+$", self.name.strip()):
            raise ValidationError("Please enter a valid name (only alphabets and spaces allowed).")
