import re
from odoo import models,fields,api
from odoo.exceptions import ValidationError

class InsauranceCompany(models.Model):

    _name = "insaurance.company"
    _description = "this model stroes the deatails of the insaurance of the company"
    _rec_name = "insaurance_name"

    insaurance_name = fields.Many2one("insaurances.insaurances",string="Name",required=True)
    phone = fields.Char(string="Phone",required=True)
    email = fields.Char(string="Email",required=True)

    @api.constrains('name')
    def validate_appointment_end_date(self):
        """this method validate the appointment end date, physician name and speciality"""
        if self.name and re.findall(r"[^a-zA-z][a-zA-z ]*", self.name):
            raise ValidationError("Please enter a vaid name")

    @api.constrains('phone')
    def _check_validations(self):
        """Function that Validate the phone no. and email"""
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError("Invalid email format. Please enter a valid email address.")

            if record.phone:
                if not re.match(r"^(0|\+91|91)?[6-9][0-9]{9}$", record.phone):
                    raise ValidationError("Contact number must start with [6,7,8,9] and must be exactly 10 numeric digits.")
            else:
                raise ValidationError("Contact number is required.")


class Insaurances(models.Model):

    _name = "insaurances.insaurances"
    _description = "model to show insaurances"
    _rec_name = "insaurance_company_name"

    number = fields.Char(default=lambda self: (''),readonly=True, copy=False,)
    insaurance_type = fields.Char(string="Insaurance Type",required=True)
    member_since = fields.Date(string="Date")
    category = fields.Char(string="Category")
    extra_info = fields.Char(string="Extra Info")
    owner = fields.Char(string="Owner")
    insaurance_company_name = fields.Char(string="Insaurance Company",required=True)
    expiration_date = fields.Date(string="Expiration Date")

    @api.model
    def create(self, vals):
        """Automatically generate a reference number for new insausrance."""
        vals['number'] = self.env['ir.sequence'].next_by_code('insaurances.insaurances')
        return super(Insaurances, self).create(vals)
