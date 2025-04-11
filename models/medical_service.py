from odoo import models,fields,api
from odoo.exceptions import ValidationError

class MedicalService(models.Model):

    _name = "medical.service"
    _description = "This Model stores the medical details of the patient"

    name = fields.Char(readonly=True, copy=False,string="Name")
    medical_description = fields.Text(string="Description")
    patient_id = fields.Many2one("patient.patient",string="Patient",required=True)
    date = fields.Datetime(string="Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string="Status", default='draft', tracking=True)
    medical_details_ids = fields.Many2many("medicine.details")

    def confirmed(self):
        """Used to change the state to confirmed"""
        self.write({
           'state': "confirmed"
        })

    def create(self, vals):
        """Automatically generate a reference number for new medical."""
        vals['name'] = self.env['ir.sequence'].next_by_code('medical.service')
        return super(MedicalService, self).create(vals)

    def action_open_medical_invoice_wizard(self):
        """This method opens the medical service invoice wizard"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Medical Service Invoice Confirmation',
            'res_model': 'medical.service.invoice',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_name': self.id},
        }

class MedicineDetails(models.Model):

    _name = 'medicine.details'
    _description = 'Store the medicine details'

    medicine_invoice = fields.Boolean(string="Invoice")
    medicine_description = fields.Char(string="Description")
    medicine_product = fields.Char(string="Product")
    medicine_quantity = fields.Integer(string="Quantity")
    medicine_from = fields.Date(string="from")
    medicine_to_date = fields.Date(string="To")

    @api.onchange('medicine_from')
    def _onchange_date(self):
        """Method to validate the medicine to date"""
        for record in self:
            if record.medicine_from > record.medicine_to_date:
                raise ValidationError("Medicine End Date can not be the date before Medicine From Date")
