from odoo import fields, models

class IntensiveCare(models.Model):
    _name = "intensive.icu"
    _description = "Intensive Model to manage Patient ICU information "

    registration_code = fields.Many2one('administration.administration',string="Registration Code")
    icu_admission = fields.Datetime(string="ICU Admission",required = True)
    patient_discharged = fields.Boolean(string="Discharged",required = True)
    patient_admitted = fields.Boolean(string="Admitted",required = True)
    admitted_duration = fields.Integer(string="Duration")
    mechenical_ventilation_history = fields.Many2many("mechnical.ventilation")

class MechnicalVentilation(models.Model):
    _name="mechnical.ventilation"
    _description = "This model handles the menchnical ventilation history"

    current_availability = fields.Boolean(string="Current")
    start_date = fields.Datetime(string="From",required=True)
    ventilation_duration = fields.Integer(string="Duration",required=True)
    ventilation_type = fields.Selection([
        ('non_invasive_pressure','Non-Invasive Positive Pressure'),
        ('invasive_pressure','Invasive Positive Pressure')
        ])
    ventilation_remarks = fields.Char(string="Remarks")

class ApacheScore(models.Model):
    _name = 'intensive.apache'
    _description = 'Model to hadle the intensive Apache Score'

    registration_code = fields.Many2one('administration.administration',string="Registration Code",required=True)
    apache_age = fields.Integer(string="Age",required=True)
    apache_date = fields.Datetime(string="Date")
    apache_temprature = fields.Float(string="Temprature",required = True)
    apache_heart_rate =fields.Float(string="Heart Rate")
    apache_flo =fields.Float(string="Flo2")
    apache_paco =fields.Float(string="paCO2")
    apache_ph =fields.Float(string="pH")
    apache_potassium =fields.Float(string="Potassium")
    apache_hematcocrit =fields.Float(string="Hematcocrit")
    apache_arf = fields.Boolean(string="ARF")
    apache_map = fields.Integer(string="MAP")
    apache_respiratory_rate = fields.Integer(string="Respiratory Rate")
    apache_pao = fields.Integer(string="PaO2")
    apache_a_do = fields.Integer(string="A-a Do2")
    apache_Sodium = fields.Integer(string="Sodium")
    apache_creatinie = fields.Float(string="Creatinie")
    apache_wbc = fields.Integer(string="WBC")
    apache_choronic_condition = fields.Boolean(string="Chronic Condition")
    apache_score = fields.Integer(string="Score",required = True)

class IntensiveEcg(models.Model):
    _name = "intensive.ecg"
    _description = "This model store the patient ECG details"

    registration_code = fields.Many2one('administration.administration',string="Registration Code",required=True)
    ecg_date = fields.Datetime(string="Date",required = True)
    ecg_lead = fields.Integer(string="Lead")
    ecg_axis = fields.Selection([
        ('normal','Normal'),('critical','Critical')
    ],required = True)
    ecg_rate = fields.Integer(string='Rate')
    ecg_pacemaker = fields.Char(string="Pacemaker")
    ecg_rhythm = fields.Selection([
        ('regular','Regular'),('daily','Daily')
    ])
    ecg_pr = fields.Integer(string="PR")
    ecg_qrs = fields.Integer(string="QRS")
    ecg_qt = fields.Integer(string="QT")
    ecg_st_segment = fields.Char(string="ST Segment")
    ecg_wave_inversion = fields.Boolean(string="T Wave Inversion")
    ecg_interpretation = fields.Selection([
        ('yes','YES'),('no','NO')
    ])

class IntensiveGcs(models.Model):
    _name = "intensive.gcs"
    _description = "This model store the patient GCS details"

    registration_code = fields.Many2one('administration.administration',string="Registration Code",required=True)
    gec_eyes = fields.Char(string="Eyes",required = True)
    gcs_motor = fields.Char(string="Motor",required=True)
    gcs_date = fields.Datetime(string="Date")
    gcs_verbal = fields.Char(string="Verbal")
    gcs_glasgow = fields.Char(string="Glasgow")
