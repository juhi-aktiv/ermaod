from odoo import models, fields


class HrInstitute(models.Model):

    _inherit = 'employee.education'

    institute_char = fields.Char(string="Institute")
