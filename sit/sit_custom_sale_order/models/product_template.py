# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_master_event = fields.Boolean(string="Master Event")

    def write(self, vals):
        res = super(ProductProduct,self).write(vals)
        product_tmpl = self.product_tmpl_id
        if product_tmpl:
            product_tmpl.is_master_event = self.is_master_event


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_master_event = fields.Boolean(string="Master Event")