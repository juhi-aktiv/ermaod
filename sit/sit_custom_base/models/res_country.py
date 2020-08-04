# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCountry(models.Model):
    _inherit = 'res.country'

    alternative_code = fields.Char('Alternative code')
