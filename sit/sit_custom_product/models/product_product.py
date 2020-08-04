# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductProduct(models.Model):

    _inherit = 'product.product'

    is_eventmodule = fields.Boolean('Eventmodule')
    is_partner_part = fields.Boolean('Partner part')
    is_sump_up = fields.Boolean('Sum up')
    is_variable = fields.Boolean('Variable')
    bestsell_number = fields.Char('Bestsell Number')
    minimal = fields.Char('Minimal')
    percent_return = fields.Float('Percent Return')
    is_creative = fields.Boolean('Creative')
    is_stocktaking = fields.Boolean('Stocktaking')


class ProductCategory(models.Model):

    _inherit = 'product.category'

    categ_code = fields.Char('Category code')