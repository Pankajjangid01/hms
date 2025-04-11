import re
from odoo import models,fields,api
from odoo.exceptions import ValidationError


class OperationalAreas(models.Model):

    _name = "operational.areas"
    _description = "This model stores and shows the operational areas in the hospital"

    name = fields.Char(string="Name",required=True)

    @api.constrains('name')
    def check_patient_name(self):
        """Method to validate the name of the patient"""
        if self.name and not re.fullmatch(r"^[A-Za-z ]+$", self.name.strip()):
            raise ValidationError("Please enter a valid name (only alphabets and spaces allowed).")

class OperationalSector(models.Model):

    _name = "operational.sector"
    _description = "Model to store the oeprational sectors"

    name = fields.Many2one("operational.areas",string="Name",required=True)
    operation_area = fields.Char(string="Operational Area",readonly=True)

    @api.onchange('name')
    def set_operational_area(self):
        """This method sets the operational area on the change of name"""
        if self.name:
            self.operation_area = self.name.name
