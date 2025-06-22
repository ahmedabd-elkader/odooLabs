from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Text()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')])
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age', store=True)
    department_id = fields.Many2one('hms.department')
    doctor_ids = fields.Many2many('hms.doctor', string="Doctors")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='Logs')

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = fields.Date.today()
                rec.age = today.year - rec.birth_date.year
            else:
                rec.age = 0

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio_required_if_pcr(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR Ratio is required if PCR is checked.")

    @api.constrains('department_id')
    def _check_closed_department(self):
        for rec in self:
            if rec.department_id and not rec.department_id.is_opened:
                raise ValidationError("You cannot assign a closed department.")

    @api.onchange('age')
    def _onchange_auto_check_pcr(self):
        for rec in self:
            if rec.age and rec.age < 30 and not rec.pcr:
                rec.pcr = True
                return {
                    'warning': {
                        'title': "PCR Auto-Checked",
                        'message': "PCR was automatically checked because the patient is under 30."
                    }
                }

    @api.onchange('state')
    def _onchange_state_log(self):
        for rec in self:
            if rec.state:
                self.env['hms.patient.log'].create({
                    'patient_id': rec.id,
                    'description': f"State changed to {rec.state}"
                })
