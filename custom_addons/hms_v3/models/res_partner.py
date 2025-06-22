from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")
    vat = fields.Char(string="Tax ID", required=True)
    website = fields.Char(string="Website")

    @api.constrains('related_patient_id', 'email')
    def _check_email_uniqueness(self):
        for rec in self:
            if rec.related_patient_id and rec.email:
                domain = [('id', '!=', rec.id), ('email', '=', rec.email), ('related_patient_id', '!=', False)]
                if self.search(domain, limit=1):
                    raise ValidationError("This email is already linked to another customer.")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("You cannot delete a customer linked to a patient.")
        return super().unlink()