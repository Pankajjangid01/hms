from odoo import fields, models, api,exceptions,_
from odoo.exceptions import ValidationError

class Administration(models.Model):

    _name = "administration.administration"
    _description = "Administration model to keep the data of patient in hospital"
    _rec_name = "registration_code"
    _inherit = ['mail.thread','mail.activity.mixin']

    registration_code = fields.Char(default=lambda self: _('New'), readonly=True)
    patient_id = fields.Many2one("patient.patient", string="Patient", required=True)
    hospital_bed_num = fields.Many2one("hospital.bed", string="Hospital Bed", required=True)
    hospitalization_date = fields.Datetime(string="Hospitalization Date",required=True)
    discharge_date = fields.Datetime(string="Expected Discharge Date",required=True)
    attending_physician = fields.Char(string="Attending Physician")
    operating_physician = fields.Char(string="Operating Physician")
    admission_type = fields.Char(string="Admission Type")
    illness_reason = fields.Char(string="Illness Reason")
    state = fields.Selection(selection=[
       ('draft', 'Free'),
       ('in_progress', 'Confirmed'),
       ('cancel', 'Cancelled'),
       ('ongoing', 'Hospitalized'),
       ('done', 'Done'),
    ], string='Status', readonly=True, copy=False,
    tracking=True, default='draft')
    transfer_history_ids = fields.One2many('bed.transfer', 'administration_id')

    @api.model
    def create(self, vals_list):
        """Automatically generate a reference number for new Administration."""
        vals_list['registration_code'] = self.env['ir.sequence'].next_by_code('administration.administration')
        return super(Administration, self).create(vals_list)

    @api.constrains('hospitalization_date')
    def check_hospitalization_date(self):
        """this method validate that the hospitalization date cannot be after the discharge date"""
        if self.hospitalization_date > self.discharge_date:
            raise ValidationError("Hospitalization date cannot be after the discharge date")

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        """Update the Attending Physician field when a patient is selected"""
        for record in self:
            if record.patient_id:
                record.attending_physician = record.patient_id.patient_primary_care_doctor_id.physisican_name.name
                record.operating_physician = record.patient_id.patient_primary_care_doctor_id.physisican_name.name
            else:
                record.attending_physician = ""

    def button_in_progress(self):
        """Used to change the state to in_progress"""
        self.write({
           'state': "in_progress"
        })

    def confirm_update(self):
        """Used to change the state to ongoing"""
        self.write({
           'state': "ongoing"
       })

    def completed(self):
        """Used to change the state to don"""
        self.write({
           'state': "done"
       })

    def button_in_draft(self):
        """Used to change the state draft"""
        self.write({
           'state': "draft"
        })

    def action_transfer_bed(self):
        """Open the Bed Transfer Wizard."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfer Bed',
            'res_model': 'hospital.bed.transfer.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_patient_id': self.id, 'default_from_bed': self.hospital_bed_num.id},
        }

class HospitalBed(models.Model):

    _name = "hospital.bed"
    _description = "Patient Allocated Bed"
    _rec_name="health_center_bed_id"

    is_allocated = fields.Boolean(string="Allocated", default=False)
    health_center_bed_id = fields.Many2one("health.center.beds", string="Health Center Bed")

class BedTransfer(models.Model):

    _name = "bed.transfer"
    _description = "Hospital Bed Transfer"

    administration_id = fields.Many2one('administration.administration', string="Patient", required=True, ondelete="cascade")
    date = fields.Datetime(string="Date", default=fields.Datetime.now, required=True)
    from_bed = fields.Many2one('hospital.bed', string="From Bed", required=True)
    to_bed = fields.Many2one('hospital.bed', string="To Bed", required=True)
    reason = fields.Text(string="Reason", required=True)

    @api.constrains('to_bed')
    def _check_bed_availability(self):
        """constraint to check the availability of the bed"""
        for record in self:
            if record.to_bed.is_allocated:
                raise exceptions.ValidationError(f"Bed {record.to_bed.health_center_bed_id} is already allocated!")

    def action_transfer(self):
        """method to transfer the patient bed"""
        if self.to_bed == self.from_bed:
            raise ValidationError("Cannot tranfer on the same bed. Please select valid bed number")

        if self.to_bed.is_allocated:
            raise exceptions.ValidationError("Selected bed is already allocated.")

        self.from_bed.is_allocated = False
        self.to_bed.is_allocated = True

        if self.from_bed.health_center_bed_id:
            self.from_bed.health_center_bed_id.status = 'free'
        if self.to_bed.health_center_bed_id:
            self.to_bed.health_center_bed_id.status = 'occupied'

        self.administration_id.hospital_bed_num = self.to_bed.id
