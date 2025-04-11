import re
from odoo import models,fields,api
from odoo.exceptions import ValidationError

class DiseasesCategory(models.Model):

    _name = "diseases.category"
    _description = "This model stores the categories of the diseases"

    name = fields.Char(string="Diseases Name",required=True)

    @api.constrains('name')
    def check_patient_name(self):
        """Method to validate the name of the patient"""
        if self.name and not re.fullmatch(r"^[A-Za-z ]+$", self.name.strip()):
            raise ValidationError("Please enter a valid name (only alphabets and spaces allowed).")

class DiseasesStructure(models.Model):

    _name = "diseases.structure"
    _description = "This model stores the categories of the diseases"

    name = fields.Char(string="Diseases Name",required=True)

    @api.constrains('name')
    def check_patient_name(self):
        """Method to validate the name of the patient"""
        if self.name and not re.fullmatch(r"^[A-Za-z ]+$", self.name.strip()):
            raise ValidationError("Please enter a valid name (only alphabets and spaces allowed).")
