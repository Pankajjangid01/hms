import re
from datetime import date
from odoo import models, fields,api
from odoo.exceptions import ValidationError

class Patient(models.Model):
    """Patient Class to handle the patient data"""

    _name = "patient.patient"
    _description = "Patient model to handle the patient data"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char("Name",required=True,tracking=True)
    patient_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender",required=True,tracking=True)
    patient_date_of_birth = fields.Date(string="Date of Birth",required=True)
    patient_maritial_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married')
    ])
    patient_address = fields.Char(string="Address")
    patient_image = fields.Binary(string="Image")
    patient_age = fields.Char(string="Age",readonly=True)
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('O', 'O'),
        ('AB', 'AB'),
    ], string="Blood Type")
    patient_rh = fields.Selection([
        ('+', '+'),
        ('-', '-')
    ], string="Rh")
    patient_ethnic_group = fields.Many2one("ethnic.group",string="Ethenic Group")
    insurances = fields.Many2one("insaurances.insaurances",string="Insurance")

    family = fields.Char(string="Family")
    patient_receivable = fields.Float(string="Receivable")
    patient_primary_care_doctor_id = fields.Many2one("physician.physician",string="Primary Care Doctor")
    patient_deceased = fields.Boolean(string="Deceased")
    disease_ids = fields.Many2many("diseases.category",string="Diseases")
    surgeries_ids = fields.One2many("patient.surgery", "patient_id", string="Surgeries")
    appointment_ids = fields.One2many("appointment.appointment","patient_id",string="Patient Appointments")
    medications_ids = fields.One2many("prescription.prescription","patient_id")
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,default=lambda self: self.env.company)
    widget_time = fields.Char(string=" Timer Widget")
    barcode = fields.Char(string="Barcode", required=True, copy=False, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('patient.patient'), readonly=True)

    @api.constrains('name')
    def check_patient_name(self):
        """Method to validate the name of the patient"""
        if self.name and not re.fullmatch(r"^[A-Za-z ]+$", self.name.strip()):
            raise ValidationError("Please enter a valid name (only alphabets and spaces allowed).")

    @api.onchange('patient_date_of_birth')
    def _onchange_compute_patient_age(self):
        """Compute patient age in years, months, and days."""
        for record in self:
            if record.patient_date_of_birth:
                today = date.today()
                dob = record.patient_date_of_birth
                if dob > today:
                    raise ValidationError("Date of Birth cannot be future date")

                years = today.year - dob.year
                months = today.month - dob.month
                days = today.day - dob.day

                if days < 0:
                    months -= 1
                    days += (date(today.year, today.month, 1) - date(today.year, today.month - 1, 1)).days

                if months < 0:
                    years -= 1
                    months += 12

                record.patient_age = f"{years} years, {months} months, {days} days"
            else:
                record.patient_age = "N/A"

    def action_download_patient_data(self):
        """Triggers the PDF report generation and download."""
        return self.env.ref('hospital_management.action_report_patient_data').report_action(self)

    def action_show_patient_appointments(self):
        """methos to show the patient appointments"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Filtered Appointments',
            'res_model': 'appointment.appointment',
            'view_mode': 'list,form',
            'target': 'current',
            'domain':[('patient_id','=',self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_show_patient_lab_result(self):
        """this method shows the lab result of the patient"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lab Reports',
            'res_model': 'lab.test.info',
            'view_mode': 'list,form',
            'target': 'current',
            'domain':[('patient_id','=',self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_show_patient_pcs_total(self):
        """this method shows the pediatrics of the patient"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'PCS',
            'res_model': 'pediatrics.pediatrics',
            'view_mode': 'list,form',
            'target': 'current',
            'domain':[('patient_id','=',self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_show_patient_prescription_orders(self):
        """this method shows the prescription of the patient"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Prescription Orders',
            'res_model': 'prescription.prescription',
            'view_mode': 'list,form',
            'target': 'current',
            'domain':[('patient_id','=',self.id)],
            'context': {'default_patient_id': self.id},
        }
