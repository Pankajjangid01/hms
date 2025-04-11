import re
from odoo import models,fields,api
from odoo.exceptions import ValidationError

class Physician(models.Model):

    _name = "physician.physician"
    _description = "This model stores the Details of physician"
    _rec_name="physisican_name"

    physisican_name = fields.Many2one("health.center",string="Name",required=True)
    physisican_id = fields.Char(default=lambda self: (''),readonly=True, copy=False,string="ID")
    institution = fields.Many2one("health.center.buildings",string="Institution",required=True)
    speciality = fields.Char(string="Speciality")
    is_available = fields.Boolean(string="Available", default=True)

    @api.model
    def create(self, vals):
        """Automatically generate a reference number for new physisican."""
        vals['physisican_id'] = self.env['ir.sequence'].next_by_code('physician.physician')
        return super(Physician, self).create(vals)

    @api.constrains('name')
    def validate_appointment_end_date(self):
        """this method validate the appointment end date, physician name and speciality"""
        if self.name and re.findall(r"[^a-zA-z][a-zA-z ]*", self.name):
            raise ValidationError("Please enter a vaid name")
