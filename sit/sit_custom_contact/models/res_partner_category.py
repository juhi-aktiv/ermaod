# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    org_code = fields.Char('Code')
