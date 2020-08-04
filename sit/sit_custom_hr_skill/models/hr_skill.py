# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'tech.tech'

    automatically_assigned_after = fields.Boolean('Automatically Assigned After')
    suitable_insert = fields.Integer('Suitable Insert')
    is_special = fields.Boolean('Special')
    is_important = fields.Boolean('Important')
