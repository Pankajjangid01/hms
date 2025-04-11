from odoo import models,fields,api

class PatientAmbulatory(models.Model):

    _name = "patient.ambulatory"
    _description = "Class to manage the patient's amublatory care"

    name = fields.Char(string="Name",required=True)
    patient_id = fields.Many2one("patient.patient",string="Patient",required=True)
    base_condition = fields.Char(string="Base Condition")
    health_proffessional = fields.Char(string="Health Professional",readonly=True)
    session = fields.Integer(string="Session #")
    start_date = fields.Datetime(string="Start",required=True)
    ordering_physician = fields.Char(string="Ordering Physician",readonly=True)
    related_evaluation = fields.Char(string="Related Evaluation",readonly=True)
    warning = fields.Boolean(string="warning")
    procedure_ids = fields.Many2many("ambulatory.care.procedure",required=True)

    @api.onchange("patient_id")
    def _onchange_patient_id(self):
        """this method sets the health proffessional and other doctor name on changing the patient id"""
        for record in self:
            if record.patient_id:
                record.health_proffessional = record.patient_id.patient_primary_care_doctor_id.physisican_name.name
                record.ordering_physician = record.patient_id.patient_primary_care_doctor_id.physisican_name.name
                record.related_evaluation = record.patient_id.patient_primary_care_doctor_id.physisican_name.name
            else:
                record.health_proffessional = ""
                record.ordering_physician = ""
                record.related_evaluation = ""

class AmbulatoryCareProcedure(models.Model):

    _name = "ambulatory.care.procedure"
    _description = "Model to store the care procedure of patient"

    procedure_code = fields.Char(string="code")
    procedure_comments = fields.Char(string="Comments")
