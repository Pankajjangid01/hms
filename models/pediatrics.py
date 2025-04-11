from odoo import models,fields,api

class Pediatrics(models.Model):

    _name = "pediatrics.pediatrics"
    _description = "Pediatrics model to store the patient pediatric symptomps"
    _rec_name="patient_id"

    patient_id = fields.Many2one("patient.patient",required=True)
    health_professional = fields.Char(string="Health Professional")
    pediatrics_symptomps_date = fields.Datetime(string="Date")
    appointment_id = fields.Char(string="Appointment",required=True)
    pcs_total = fields.Integer(string="PCS Total")
    less_inerested_in_school = fields.Boolean(string="Less interested in school")
    symptomps_complain = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Complains of aches and pains")
    spend_more_time_alone = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Spends more time alone")
    patient_tires_easily = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Tires easily,has little energy")
    unable_to_sit_still = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Fidgety, unable to sit still")
    has_trouble_with_teacher = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Has trouble with teaher")
    acts_as_driven_by_motor = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Acts as if driven by a motor")
    daydreams_too_much = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Daydreams too much")
    school_grades_dropping = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="School grades Dropping")
    is_down = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Is down on him or herself")
    visits_the_docter = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),('daily','daily')
        ],string="Visits the docter with doctor finding")
    has_trouble_sleeping = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Has touble sleeping")
    worries_alote = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Worries a lot")
    wants_to_be_with_you = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Wants to be with you more than before")
    feels_bad = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Feels he or she is bad")
    takes_unnescessary_risks = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Takes unnecssary risks")
    get_hurts_often = fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('daily','daily')
        ],string="Get hurts often")

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        """Update the health professional field and get the latest appointment"""
        for record in self:
            if record.patient_id:
                record.health_professional = record.patient_id.patient_primary_care_doctor_id.physisican_name.name
            else:
                record.health_professional = ""

            patient_appointments = self.env["appointment.appointment"].search(
                [('patient_id', '=', record.patient_id.id)]
            )

            if patient_appointments:
                latest_appointment = patient_appointments.sorted('appointment_date', reverse=True)[0]
                record.appointment_id = latest_appointment.appointment_id
            else:
                record.appointment_id = ""
