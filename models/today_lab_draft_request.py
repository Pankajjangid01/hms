from odoo import models,fields,api

class TodayLabRequest(models.Model):

    _name = "today.lab.request"
    _description = "This model shows today's draft lab request"

    request = fields.Char(string="Request")
    test_type = fields.Char(string="Test Type",readonly = True,required=True)
    test_date = fields.Datetime(string="Date")
    patient_id = fields.Many2one("patient.patient",string="Patient",required=True)
    patient_doctor = fields.Char(string="Doctor",readonly = True,required=True)
    state = fields.Selection([
        ('pending','Pending'),
        ('completd','Completed')
    ],required=True)

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        """Get the test type of the seleceted patient"""
        for record in self:
            if record.patient_id:
                patient_test_type = self.env['draft.laboratory'].search([('patient_id','=',self.patient_id.id)])
                record.test_type = patient_test_type.test_type_name.name
                record.patient_doctor = patient_test_type.patient_doctor
            else:
                record.patient_doctor = ""
