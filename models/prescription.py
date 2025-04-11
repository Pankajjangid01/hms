import re
from odoo import models, fields,api
from odoo.exceptions import ValidationError

class Prescription(models.Model):
    """Prescription Class to handle the prescription of patient"""

    _name = "prescription.prescription"
    _description = "Prescription model to manage the prescription of the patient"
    _rec_name = "prescription_id"
    _inherit = ['mail.thread','mail.activity.mixin']

    patient_id = fields.Many2one("patient.patient", string="Patient",required=True)
    prescription_date = fields.Datetime(string="Prescription Date")
    health_center_name = fields.Char(string="Phramacy",readonly=True)
    prescription_id = fields.Char(default=lambda self: ('New'),readonly=True, copy=False,string="Prescription Id")
    login_user = fields.Many2one("res.users",default=lambda self:self.env.user, string="Login User",required=True)
    prescribing_doctor = fields.Char(string="Prescribing Doctor",readonly=True)
    invoice_to_insurance = fields.Boolean(string="Invoice to Insurance")
    prescription_details_ids = fields.Many2many("medicine.medicine",required=True)

    @api.model
    def create(self, vals):
        """Automatically generate a reference number for new Administration."""
        vals['prescription_id'] = self.env['ir.sequence'].next_by_code('prescription.prescription')
        return super(Prescription, self).create(vals)

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        """method to set the patient's doctor and hospital names"""
        if self.patient_id:
            self.health_center_name = self.patient_id.patient_primary_care_doctor_id.institution.name
            self.prescribing_doctor = self.patient_id.patient_primary_care_doctor_id.physisican_name.name

    def prescription_report_download(self):
        """Triggers the PDF report generation and download."""
        return self.env.ref('hospital_management.action_report_prescription_data').report_action(self)

    @api.constrains('appointment_end','physician','speciality')
    def validate_appointment_end_date(self):
        """this method validate the appointment end date, physician name and speciality"""
        if self.prescribing_doctor and re.findall(r"[^a-zA-z][a-zA-z ]*", self.prescribing_doctor):
            raise ValidationError("Please enter a vaid name")

    def action_open_prescription_invoice_wizard(self):
        """this method open the prescription invoice confirmation wizard"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Prescription Invoice Confirmation',
            'res_model': 'prescription.invoice.confirmation.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_prescription_id': self.id},
        }

class Medicines(models.Model):
    """Class to sotre the medicine of the patient and their details"""

    _name="medicine.medicine"
    _description = "Medicine model to manage the medicine of the patient"

    print_medicine = fields.Boolean(string="Print")
    medicament_name = fields.Many2one("medicament.misc",string="Medicament")
    indication = fields.Char(string="Indication")
    medicine_dose = fields.Float(string="Dose")
    medicine_dose_units = fields.Many2one("medicament.units",string="Medicine Dose Unit")
    medicine_from = fields.Char(string="From")
    medince_frequency = fields.Integer(string="Frequency")
    medicine_quantity = fields.Integer(string="Quantity")
    treatment_duration = fields.Integer(string="Treatment Duration")
    treatment_period = fields.Selection([
        ('days','Days'),
        ('week','Weeks'),
        ('month','Months')
    ],string="Treatment Period")
    comment = fields.Char("Comment")
    allow_substituion = fields.Boolean("Allow Substitution")
