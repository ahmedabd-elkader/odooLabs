from odoo import models, fields

class Doctor(models.Model):
    _name = 'hms.doctors'
    _description = 'Doctor'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Binary(string="Image")
    patient_ids = fields.Many2many('hms.patient', string="Patients")