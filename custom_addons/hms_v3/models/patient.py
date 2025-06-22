import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    first_name = fields.Char()
    last_name = fields.Char()
    email = fields.Char(string="Email", required=True)
    birth_date = fields.Date()
    age = fields.Integer(compute="_compute_age", store=True)
    history = fields.Text()
    cr_ratio = fields.Float(string='CR RATIO')
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O')
    ], string="Blood Type")
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()

    department_id = fields.Many2one('hms.department', string="Department")
    doctor_ids = fields.Many2many('hms.doctors', string="Doctors")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')

    state_logs = fields.One2many('hms.patient.log', 'patient_id', string="State Logs")

    @api.constrains('email')
    def _check_valid_unique_email(self):
        for rec in self:
            if not rec.email or not re.match(EMAIL_REGEX, rec.email):
                raise ValidationError("Please enter a valid email address.")
            existing = self.search([('email', '=', rec.email), ('id', '!=', rec.id)], limit=1)
            if existing:
                raise ValidationError("Email must be unique. This email is already used.")

    @api.depends("birth_date")
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = fields.Date.today()
                rec.age = today.year - rec.birth_date.year - ((today.month, today.day) < (rec.birth_date.month, rec.birth_date.day))
            else:
                rec.age = 0

    @api.onchange("age")
    def _onchange_age(self):
        for rec in self:
            if rec.age and rec.age < 30 and not rec.pcr:
                rec.pcr = True
                return {
                    "warning": {
                        "title": "PCR Automatically Checked",
                        "message": "PCR field has been checked automatically because age is below 30."
                    }
                }

    def write(self, vals):
        res = super().write(vals)
        if 'state' in vals:
            for rec in self:
                self.env['hms.patient.log'].create({
                    'description': f"State changed to {vals['state']}",
                    'patient_id': rec.id
                })
        return res