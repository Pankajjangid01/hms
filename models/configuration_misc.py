from odoo import models, fields, api

class MedicamentsMisc(models.Model):
    _name = "medicament.misc"
    _description = "Model to store the details of medicines"

    name = fields.Char(string="Name", required=True)
    active_component = fields.Char(string="Active Component")
    category_id = fields.Many2one("diseases.category", string="Category")
    quantity_available = fields.Integer(string="Quantity Available")
    therapeutic_effect = fields.Char(string="Therapeutic Effect")
    pregnancy_warning = fields.Boolean(string="Pregnancy Warning")
    price = fields.Integer(string="Price")

    @api.model
    def create(self, vals):
        """method to create the medicine in the medicament list"""
        record = super(MedicamentsMisc, self).create(vals)
        self.env["medicament.list"].create({
            "name": record.name,
            "active_component": record.active_component,
            "category": record.category_id.name if record.category_id else "",
            "quantity_available": record.quantity_available,
            "therapeutic_effect": record.therapeutic_effect,
            "pregnancy_warning": "Yes" if record.pregnancy_warning else "No",
            "price": record.price,
        })
        return record

    def write(self, vals):
        """method to update the medicine details on change in medicament"""
        res = super(MedicamentsMisc, self).write(vals)
        for record in self:
            medicament_list = self.env["medicament.list"].search([("name", "=", record.name)])
            if medicament_list:
                medicament_list.write({
                    "name": record.name,
                    "active_component": record.active_component,
                    "category": record.category_id.name if record.category_id else "",
                    "quantity_available": record.quantity_available,
                    "therapeutic_effect": record.therapeutic_effect,
                    "pregnancy_warning": "Yes" if record.pregnancy_warning else "No",
                    "price": record.price,
                })
        return res

    def unlink(self):
        """method to delete the medicine from medicament list"""
        for record in self:
            self.env["medicament.list"].search([("name", "=", record.name)]).unlink()
        return super(MedicamentsMisc, self).unlink()

class MedicalSpeciality(models.Model):

    _name = "medical.speciality"
    _description = "specialities of doctor"
    _rec_name = "speciality_description"

    speciality_description = fields.Char(string="Description",required=True)
    code = fields.Char(default=lambda self: (''),readonly=True, copy=False)

    @api.model
    def create(self, vals):
        """Automatically generate a reference number for new speciality."""
        vals['code'] = self.env['ir.sequence'].next_by_code('medical.speciality')
        return super(MedicalSpeciality, self).create(vals)


class MedicamentUnits(models.Model):

    _name = "medicament.units"
    _description = "This model store the units of the medicine"
    _rec_name = "unit"

    unit = fields.Char(string="Unit",required=True)
    description = fields.Char(string="Description",store=True)

    @api.onchange('unit')
    def _onchange_unit(self):
        """This method set the description on changing unit"""
        if self.unit:
            self.description = self.unit

class Occupation(models.Model):

    _name = "occupation.occupation"
    _description = "Creates the Occupations"

    occupation_name = fields.Char(string="Occupation",required=True)
    code = fields.Char(string="Code",store = True)

    @api.onchange('occupation_name')
    def _onchange_unit(self):
        """This method set the code on changing occupation"""
        if self.occupation:
            self.code = self.occupation
