from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Appointments(models.Model):
    """Appointment Class to create the appointment dof the patient"""

    _name = "appointment.appointment"
    _description = "Appointment model to handle the patient appointments"
    _rec_name = "appointment_id"
    _inherit = ['mail.thread','mail.activity.mixin']

    appointment_id = fields.Char(default=lambda self: ('New'), readonly=True, copy=False,)
    patient_id = fields.Many2one('patient.patient',required=True)
    physician = fields.Char(string="Physician",readonly = True)
    speciality = fields.Char(string="Speciality",readonly = True)
    appointment_date = fields.Datetime(string="Appointment Date",required=True)
    appointment_end = fields.Datetime(string="Appointment End",required=True)
    appointment_duration = fields.Float(string="Duration (Hours)")
    patient_status = fields.Selection([
        ('Outpatient','Outpatient'),
        ('critical','Critical'),
        ('stable','Stable'),
        ('good','Good')
    ], string="Patient Status")
    invoice_exempt = fields.Boolean(string="Invoice Exempt")
    appointment_status = fields.Selection([
        ('completed',"Invoiced"),
        ('pending','To be invoiced')
    ], string="Status")
    validity_date = fields.Date(string="Validity Date")
    health_center_name = fields.Char(string="Health Center",readonly = True)
    inpatient_registration = fields.Char(string="Inpatient Registration",readonly=True,store=True)
    urgency_level = fields.Selection([
        ('urgent','Urgent'),
        ('good','Good')
    ], string="Urgency Level")
    invoice_to_insaurance = fields.Boolean(string="Invoice to Insurance")
    consulting_service = fields.Selection([
        ('consulting','Consulting'),
        ('clinical','Clinical Consulting'),
        ('operations','Operations Consulting')
    ], string="Consulting Service")

    @api.model
    def create(self, vals_list):
        """Automatically generate a reference number for new Administration."""
        vals_list['appointment_id'] = self.env['ir.sequence'].next_by_code('appointment.appointment')
        return super(Appointments, self).create(vals_list)

    @api.onchange('appointment_date', 'appointment_end')
    def _onchange_compute_duration(self):
        """Compute appointment duration in hours"""
        for record in self:
            if record.appointment_date and record.appointment_end:
                if record.appointment_date > record.appointment_end:
                    raise ValidationError("Appointment start Date cannot be after the appointment end date")

                datetime_difference = record.appointment_end - record.appointment_date
                record.appointment_duration = datetime_difference.total_seconds() / 3600
            else:
                record.appointment_duration = 0

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        """method to set the value of physician,speciality,health center name on the change of the patient"""
        if self.patient_id:
            self.health_center_name = self.patient_id.patient_primary_care_doctor_id.institution.name
            self.physician = self.patient_id.patient_primary_care_doctor_id.physisican_name.name
            self.speciality = self.patient_id.patient_primary_care_doctor_id.speciality
            inpatient_code = self.env['administration.administration'].search([('patient_id','=',self.patient_id.id)])
            if not inpatient_code:
                raise ValidationError("Please Hospitalize the patient")
            self.inpatient_registration = inpatient_code.registration_code

    def action_download_appointment_report(self):
        """Triggers the PDF report generation and download."""
        return self.env.ref('hospital_management.action_report_appointment_data').report_action(self)

    @api.constrains('appointment_end','physician','speciality')
    def validate_appointment_end_date(self):
        """Method to validate the appointment end date , phyisician name and speciality"""
        if self.appointment_end < self.appointment_date:
            raise ValidationError("Appointment End Date can not be the date before Appointment Start Date")

    def action_open_invoice_wizard(self):
        """this method open the invoice confermation wizard"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Invoice Confirmation',
            'res_model': 'invoice.confirmation.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_appointment_id': self.id},
        }
    
    @api.constrains('physician')
    def check_physician_availability(self):
        """Ensure appointment is created only if physician is available."""
        for record in self:
            if record.patient_id and record.patient_id.patient_primary_care_doctor_id:
                physician = record.patient_id.patient_primary_care_doctor_id
                if not physician.is_available:
                    raise ValidationError(f"Physician '{physician.physisican_name.name}' is currently not available for appointments.")
                else:
                    physician.is_available = False
