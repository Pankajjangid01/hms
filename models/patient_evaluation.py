from odoo import models,fields,api

class PatientEvaluation(models.Model):

    _name = "patient.evaluation"
    _description = "This model shows the patient evaluation information"

    patient_id = fields.Many2one("patient.patient",string="Patient",required=True)
    start_evalutaion = fields.Datetime(string="Start Evaluation")
    chief_comnplaint = fields.Char(string="Injury")
    evaluation_type = fields.Char(string="Type")
    end_of_evaluation = fields.Datetime(string="End of Evaluation")
    doctor = fields.Char(string="Doctor")
    body_mass_index = fields.Float(string="Body Mass Index")
    systolic_pressure = fields.Float(string="Systolic Pressure")
    diastolic_pressure = fields.Float(string="Diastolic Pressure")
    presumptive_diagnosis = fields.Integer(string="Presumptive Diagnosis")
    next_appointment = fields.Char(string="Next Appointment")

    @api.onchange("patient_id")
    def _onchange_patient_id(self):
        """sets the doctor name on change of the patient name"""
        for record in self:
            if record.patient_id:
                record.doctor = record.patient_id.patient_primary_care_doctor_id.physisican_name.name
            else:
                record.doctor = ""
