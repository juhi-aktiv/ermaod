# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    department = fields.Char('Department')
    is_newsletter = fields.Boolean('Newsletter')
    is_newsletter_pers = fields.Boolean('Newsletter Pers')
    mail_merge = fields.Boolean('Mail merge')
    fax = fields.Char('Fax')
