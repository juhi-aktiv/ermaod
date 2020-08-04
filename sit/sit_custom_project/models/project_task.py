# -*- coding: utf-8 -*-

from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    days_before = fields.Char('Days before')
    offer_date = fields.Boolean('Offer date')
