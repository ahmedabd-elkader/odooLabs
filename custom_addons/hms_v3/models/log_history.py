from odoo import models, fields

class PatientLog(models.Model):
    _name = "hms.patient.log"
    _description = "Patient State Change Log"

    description = fields.Text()
    patient_id = fields.Many2one('hms.patient')
    create_date = fields.Datetime(string="Created On", readonly=True)
    create_uid = fields.Many2one('res.users', string="Created By", readonly=True)