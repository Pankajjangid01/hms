from odoo import models,fields,api
from odoo.exceptions import ValidationError
import re

class Families(models.Model):

    _name = "patient.family"
    _description = "Model to store the patient family data"

    name_id = fields.Many2one("patient.patient",string="Name")
    operational_sector = fields.Char(string="Operational Sector")
    members_ids = fields.Many2many("patient.member","patient_family_rel") 

class Members(models.Model):

    _name = "patient.member"
    _description = "patient family members details"

    name = fields.Char(string="Name")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    
    @api.constrains('phone')
    def _check_validations(self):
        """Function to validate the Contact number"""
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError("Invalid email format. Please enter a valid email address.")
            if record.contact:
                if not re.match(r"^(0|\+91|91)?[6-9][0-9]{9}$", record.phone):
                    raise ValidationError("Contact number must start with [6,7,8,9] and must be exactly 10 numeric digits.")
            else:
                raise ValidationError("Contact number is required.")