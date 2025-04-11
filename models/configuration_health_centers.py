from odoo import models, fields,api
from odoo.exceptions import ValidationError
import re

class HealthCenterBuildings(models.Model):

    _name = "health.center.buildings"
    _description = "Model to shows the health center building"

    name = fields.Char(string="Name",required=True)
    building_institution = fields.Char(string="Institute",required=True)


class HealthCenter(models.Model):

    _name = "health.center"
    _description = "Model to store the name,phone no. and email of doctor"

    name = fields.Char(string="Name",required=True)
    phone = fields.Char(string="Phone no.",required=True)
    email = fields.Char(string="Email",required=True)

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
    

class HealthCenterUnits(models.Model):

    _name = "health.center.units"
    _description = "Model to show health center units"

    name = fields.Char(string="Name",required=True)
    institution = fields.Many2one("health.center.buildings",string="Instituion",required=True)


class HealthCenterWards(models.Model):

    _name = "health.center.wards"
    _description = "This model store the wards in the hospital"

    name = fields.Char(string="Name",required=True)
    no_of_wards = fields.Integer(string="Number of wards",required=True)
    gender = fields.Selection([
        ('men','Men Ward'),
        ('women','Women Ward'),
        ('unisex','Unisex')
    ],string="Gender",required=True)

    institution = fields.Many2one("health.center.buildings",string="Institution",required=True)
    status = fields.Selection([
        ('available','Bed Available'),
        ('full','Full')
    ],string="Status",required=True)


class HealthCenterBeds(models.Model):

    _name = "health.center.beds"
    _description = "This model stores the bed information of the ward in hospital"

    name = fields.Char(string="Bed",required=True)
    ward_name = fields.Many2one("health.center.wards",string="Ward",required=True)
    status = fields.Selection([
        ('free','Free'),
        ('occupied','Occupied')
    ],string="Status",required=True, default=lambda self:"free")
    

class HospitalOpeningRooms(models.Model):

    _name = "hospital.opening.rooms"
    _description = "Model to store the Opening rooms in the hospital"

    name = fields.Char(string="Name",required=True)
    institution = fields.Many2one("health.center.buildings",string="Building",required=True)
    unit = fields.Many2one("health.center.units",string="Units",required=True)
