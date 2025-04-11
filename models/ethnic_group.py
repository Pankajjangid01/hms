import re
from odoo import models,fields,api
from odoo.exceptions import ValidationError


class EthnicGroup(models.Model):

    _name = "ethnic.group"
    _description = "Creates the ethnic group for the patient"
    _rec_name = "ethnic_group"

    ethnic_group = fields.Char(string="Ethnic Group",required=True)
    code = fields.Char(string="Code",required=True)

    @api.constrains('ethnic_group')
    def check_patient_name(self):
        """Method to validate the name of the patient"""
        if self.ethnic_group and not re.fullmatch(r"^[A-Za-z ]+$", self.ethnic_group.strip()):
            raise ValidationError("Please enter a valid name (only alphabets and spaces allowed).")
