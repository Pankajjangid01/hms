import re
from odoo import models,fields,api
from odoo.exceptions import ValidationError

class Medicaments(models.Model):
    
    _name = "medicaments.medicaments"
    _description = "Model to store the medicaments data"

    route = fields.Char(string="Route",required=True)
    code = fields.Char(string="Code")

    @api.onchange("route")
    def _onchange_route(self):
        """method to set the value of the code on the change of the route"""
        for record in self:
            if record.route:
                record.code = record.route
            else:
                record.code = ""

class MedicamentForm(models.Model):

    _name = "medicament.form"
    _description = "Model for the medicament form"

    medicament_from = fields.Char(string="From",required=True)
    medicament_code = fields.Char(string="Code")

    @api.onchange("medicament_from")
    def _onchange_medicament_from(self):
        """method to set the medicament code"""
        for record in self:
            if record.medicament_from:
                record.medicament_code = record.medicament_from
            else:
                record.medicament_code = ""

class MedicalCategories(models.Model):

    _name = "medical.categories"
    _description = "Model to store the categories of medicine"

    name = fields.Char(string="Category Name",required=True)

    @api.constrains('name')
    def validate_appointment_end_date(self):
        """this method ensure the valid category name"""
        if self.name and re.findall(r"[^a-zA-z][a-zA-z ]*", self.name):
            raise ValidationError("Please enter a vaid name")
