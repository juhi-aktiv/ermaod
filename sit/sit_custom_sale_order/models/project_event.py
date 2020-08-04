# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (C) Solvate Informationstechnologie GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models, _


class ProjectEvent(models.Model):
    _name = 'project.event'
    _description = 'Project Event Model'

    is_duplicate = fields.Boolean(string="Duplicate")
    custom_sequence = fields.Integer(string="Sequence", default=0,store=True)
    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    name = fields.Char(string="Event")
    product_id = fields.Many2one('product.product')
    is_inactive = fields.Boolean('Set as Inactive')
    sale_order_line_ids = fields.Many2one('sale.order.line',
                                         string="Sale Order Line")
    color = fields.Char(string='Color', store=True)

    @api.onchange('from_date', 'to_date')
    def check_dates(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            self.to_date = self.from_date
