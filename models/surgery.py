from odoo import models,fields,api

class PatientSurgery(models.Model):

    _name = "patient.surgery"
    _description = "This model contains the surgery details of the patient"

    patient_id = fields.Many2one("patient.patient",string="Patient Name",required=True,ondelete="cascade")
    procedure_description = fields.Char(string="Description",readonly=True)
    procedure_code = fields.Char(string="Code",readonly=True)
    base_condition = fields.Char(string="Base Condition",readonly=True)
    surgery_classification = fields.Selection([
        ('required','Required'),
        ('not-required','Not Required')
    ])
    date_of_surgery = fields.Datetime(string="Date of surgrey")
    patient_age = fields.Char(string="Patient Age",readonly=True)
    surgeon = fields.Char(string="Surgeon",readonly=True)
    extra_info = fields.Text(string="Extra Info")

    @api.onchange("patient_id")
    def _onchange_patient_id(self):
        """sets the the fields value based on the change of patient name"""
        for record in self:
            if record.patient_id:
                patient_nursing_details = self.env['patient.ambulatory'].search([('patient_id','=',record.patient_id.id)])
                record.base_condition = patient_nursing_details.base_condition
                record.procedure_description = patient_nursing_details.procedure_ids.procedure_comments
                record.procedure_code = patient_nursing_details.procedure_ids.procedure_comments
                record.patient_age = record.patient_id.patient_age
                record.surgeon = record.patient_id.patient_primary_care_doctor_id.physisican_name.name
