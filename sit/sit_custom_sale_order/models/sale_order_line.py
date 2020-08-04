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
from datetime import datetime
from odoo.exceptions import UserError
from odoo.http import request
from datetime import date, timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_order_tmpl_ids = fields.Many2many('sale.order.template', string="Quotation Template", required=True, ondelete='cascade', index=True)
    event_product_available = fields.Boolean(string="Event Product Available", compute="_compute_event_product")

    # def _write(self, values):
    #     project_event = self.env['project.event']
    #     for line in self.order_line:
    #         if line.is_master_event:
    #             new_ids = self.order_line.filtered(
    #                 lambda x: x.custom_sequence_new == line.custom_sequence_new and not x.is_master_event)
    #             for o_line in new_ids:
    #                 filter_rec = o_line.event_id.filtered(lambda x: x.from_date != line.event_id.filtered(lambda y: y.from_date))
    #                 filter_rec_to = o_line.event_id.filtered(lambda x: x.to_date != line.event_id.filtered(lambda y: y.to_date))
    #                 if len(line.event_id) != len(o_line.event_id) or filter_rec or filter_rec_to:
    #
    #                     inactive_ids = o_line.event_id.filtered(lambda x: x.is_inactive)
    #                     event_lines = []
    #                     datas = {}
    #                     for data in line.event_id:
    #                         o_line.product_uom_qty = line.product_uom_qty
    #                         existing_event_lines = []
    #                         existing_dates = []
    #
    #                         for existing_sequence in o_line.event_id:
    #                             existing_event_lines.append(existing_sequence.custom_sequence)
    #                         for existing_fdate in o_line.event_id:
    #                             existing_dates.append(existing_fdate.from_date)
    #
    #                         for event_ids in o_line.event_id:
    #                             if event_ids.custom_sequence == data.custom_sequence:
    #                                 if event_ids.from_date != data.from_date:
    #                                     o_line.event_id = [(1, event_ids.id, {'from_date': data.from_date})]
    #                                 if event_ids.to_date != data.to_date:
    #                                     o_line.event_id = [(1, event_ids.id, {'to_date': data.to_date})]
    #
    #
    #                         if o_line.product_uom_qty > len(o_line.event_id):
    #                             if data.custom_sequence not in existing_event_lines:
    #                                 datas = {
    #                                     'custom_sequence': data.custom_sequence,
    #                                     'name': data.name,
    #                                     'from_date': data.from_date,
    #                                     'to_date': data.to_date,
    #                                 }
    #                                 if o_line.product_id:
    #                                     datas.update({
    #                                         'product_id': o_line.product_id.id,
    #                                     })
    #                                 event_lines.append((0, 0, datas))
    #                     o_line.event_id = event_lines
    #
    #                     for event_line in o_line.event_id:
    #                         duplicate_records = []
    #                         duplicate_torecords = []
    #                         duplicate_event_record = project_event.search([
    #                             ('sale_order_line_ids','!=',o_line.id),
    #                             ('product_id', '=', o_line.product_id.id),
    #                         ])
    #                         for devent in duplicate_event_record:
    #                             duplicate_records.append(devent.from_date)
    #                             duplicate_torecords.append(devent.to_date)
    #                         if duplicate_records and duplicate_torecords:
    #                             min_duplicate_records = min(duplicate_records)
    #                             max_duplicate_records = max(duplicate_torecords)
    #                             start = min_duplicate_records
    #                             end = max_duplicate_records
    #                             # final_dates = []
    #                             final_dates = [date.fromordinal(i) for i in range(start.toordinal(), end.toordinal())]
    #                             if event_line.from_date in final_dates or event_line.to_date in final_dates:
    #                                 event_line.is_duplicate = True
    #                                 # o_line.is_duplicate = True
    #                             for o_line_danger in o_line.event_id:
    #                                 if o_line_danger.is_duplicate:
    #                                     o_line.is_duplicate = True
    #                                 if o_line_danger.is_inactive:
    #                                     o_line.is_inactive = True
    #                         if event_line in inactive_ids:
    #                             event_line.is_inactive = True
    #                             event_line.is_duplicate = False
    #                             # o_line.is_inactive = True
    #                             # o_line.is_duplicate = False
    #                         for o_line_danger in o_line.event_id:
    #                             if o_line_danger.is_inactive :
    #                                 o_line.is_inactive = True
    #                             if o_line_danger.is_duplicate:
    #                                 o_line.is_duplicate = True
    #                                 o_line.is_inactive = False
    #                                 # if len(line.event_id) < len(o_line.event_id):
    #                                 #     o_line.product_uom_qty = len(o_line.event_id)
    #
    #                                 # if len(line.event_id) < len(o_line.event_id):
    #                                 #     o_line.product_uom_qty = len(o_line.event_id)
    #     return super(SaleOrder, self)._write(values)
    def _write(self, values):
        project_event = self.env['project.event']
        for line in self.order_line:
            if line.is_master_event:
                new_ids = self.order_line.filtered(
                    lambda x: x.custom_sequence_new == line.custom_sequence_new and not x.is_master_event)
                for o_line in new_ids:
                    filter_rec = o_line.event_id.filtered(lambda x: x.from_date != line.event_id.filtered(lambda y: y.from_date))
                    filter_rec_to = o_line.event_id.filtered(lambda x: x.to_date != line.event_id.filtered(lambda y: y.to_date))
                    if len(line.event_id) != len(o_line.event_id) or filter_rec or filter_rec_to:

                        inactive_ids = o_line.event_id.filtered(lambda x: x.is_inactive)
                        event_lines = []
                        datas = {}
                        for data in line.event_id:
                            o_line.product_uom_qty = line.product_uom_qty
                            existing_event_lines = []
                            existing_dates = []

                            for existing_sequence in o_line.event_id:
                                existing_event_lines.append(existing_sequence.custom_sequence)
                            for existing_fdate in o_line.event_id:
                                existing_dates.append(existing_fdate.from_date)

                            for event_ids in o_line.event_id:
                                if event_ids.custom_sequence == data.custom_sequence:
                                    if event_ids.from_date != data.from_date:
                                        o_line.event_id = [(1, event_ids.id, {'from_date': data.from_date})]
                                    if event_ids.to_date != data.to_date:
                                        o_line.event_id = [(1, event_ids.id, {'to_date': data.to_date})]


                            if o_line.product_uom_qty > len(o_line.event_id):
                                if data.custom_sequence not in existing_event_lines:
                                    datas = {
                                        'custom_sequence': data.custom_sequence,
                                        'name': data.name,
                                        'from_date': data.from_date,
                                        'to_date': data.to_date,
                                    }
                                    if o_line.product_id:
                                        datas.update({
                                            'product_id': o_line.product_id.id,
                                        })
                                    event_lines.append((0, 0, datas))
                        o_line.event_id = event_lines

                        for event_line in o_line.event_id:
                            duplicate_records = []
                            duplicate_torecords = []
                            duplicate_event_record = project_event.search([
                                ('sale_order_line_ids','!=',o_line.id),
                                ('product_id', '=', o_line.product_id.id),
                            ])
                            for devent in duplicate_event_record:
                                duplicate_records.append(devent.from_date)
                                duplicate_torecords.append(devent.to_date)
                            if duplicate_records and duplicate_torecords:
                                min_duplicate_records = min(duplicate_records)
                                max_duplicate_records = max(duplicate_torecords)
                                start = min_duplicate_records
                                end = max_duplicate_records
                                # final_dates = []
                                final_dates = [date.fromordinal(i) for i in range(start.toordinal(), end.toordinal())]
                                if event_line.from_date in final_dates or event_line.to_date in final_dates:
                                    event_line.is_duplicate = True
                                    # o_line.is_duplicate = True
                                for o_line_danger in o_line.event_id:
                                    if o_line_danger.is_duplicate:
                                        o_line.is_duplicate = True
                                    if o_line_danger.is_inactive:
                                        o_line.is_inactive = True
                            if event_line in inactive_ids:
                                event_line.is_inactive = True
                                event_line.is_duplicate = False
                                # o_line.is_inactive = True
                                # o_line.is_duplicate = False
                            for o_line_danger in o_line.event_id:
                                if o_line_danger.is_inactive :
                                    o_line.is_inactive = True
                                if o_line_danger.is_duplicate:
                                    o_line.is_duplicate = True
                                    o_line.is_inactive = False
                                    # if len(line.event_id) < len(o_line.event_id):
                                    #     o_line.product_uom_qty = len(o_line.event_id)

                                    # if len(line.event_id) < len(o_line.event_id):
                                    #     o_line.product_uom_qty = len(o_line.event_id)
        return super(SaleOrder, self)._write(values)

    @api.onchange('order_line')
    def master_order_onchange(self):
        project_event = self.env['project.event']
        for line in self.order_line:
            if line.is_master_event:
                new_ids = self.order_line.filtered(
                    lambda x: x.custom_sequence_new == line.custom_sequence_new and not x.is_master_event)
                for o_line in new_ids:
                    o_line.product_uom_qty = line.product_uom_qty
                    inactive_ids = o_line.event_id.filtered(lambda x: x.is_inactive)
                    event_lines = []
                    datas = {}

                    for data in line.event_id:
                        existing_event_lines = []
                        for existing_sequence in o_line.event_id:
                            existing_event_lines.append(existing_sequence.custom_sequence)
                        for event_ids in o_line.event_id:
                            if event_ids.custom_sequence == data.custom_sequence:
                                if event_ids.from_date != data.from_date:
                                    o_line.event_id = [(1, event_ids.id, {'from_date': data.from_date})]
                                if event_ids.to_date != data.to_date:
                                    o_line.event_id = [(1, event_ids.id, {'to_date': data.to_date})]

                        if int(line.product_uom_qty) < len(o_line.event_id):
                            existing_main_event_lines = []
                            for existing_main_sequence in data:
                                existing_main_event_lines.append(existing_main_sequence.custom_sequence)
                            unlink_list = []
                            for event_i in o_line.event_id:
                                if event_i.custom_sequence not in existing_main_event_lines:
                                    unlink_list.append(event_i)
                                o_line.event_id = [(2, c.id) for c in unlink_list]

                        if o_line.product_uom_qty > len(o_line.event_id):
                            if data.custom_sequence not in existing_event_lines:
                                datas = {
                                    'custom_sequence': data.custom_sequence,
                                    'name': data.name,
                                    'from_date': data.from_date,
                                    'to_date': data.to_date,
                                }
                                if o_line.product_id:
                                    datas.update({
                                        'product_id': o_line.product_id.id,
                                    })
                                event_lines.append((0, 0, datas))
                    o_line.event_id = event_lines

                    for event_line in o_line.event_id:
                        duplicate_records = []
                        duplicate_torecords = []
                        date_from = event_line.from_date
                        duplicate_event_record = project_event.search([
                                                # ('sale_order_line_ids', '!=', o_line.id),
                                                ('product_id', '=', o_line.product_id.id),
                                            ])

                        for devent in duplicate_event_record:
                            duplicate_records.append(devent.from_date)
                            duplicate_torecords.append(devent.to_date)
                        if duplicate_records and duplicate_torecords:
                            min_duplicate_records = min(duplicate_records)
                            max_duplicate_records = max(duplicate_torecords)
                            # final_dates = []
                            final_dates = [date.fromordinal(i) for i in range(min_duplicate_records.toordinal(), max_duplicate_records.toordinal())]
                            event_dates = [date.fromordinal(j) for j in range(event_line.from_date.toordinal(), event_line.to_date.toordinal())]
                            if any(elem in event_dates for elem in final_dates) or any(elem1 in event_dates for elem1 in final_dates):
                                    event_line.is_duplicate = True
                                # o_line.is_duplicate = True
                            for o_line_danger in o_line.event_id:
                                if o_line_danger.is_duplicate:
                                    o_line.is_duplicate = True
                                if o_line_danger.is_inactive:
                                    o_line.is_inactive = True
                        if event_line in inactive_ids:
                            event_line.is_inactive = True
                            event_line.is_duplicate = False
                            # o_line.is_inactive = True
                            # o_line.is_duplicate = False
                        for o_line_danger in o_line.event_id:
                            if o_line_danger.is_duplicate:
                                o_line.is_duplicate = True
                                # if len(line.event_id) < len(o_line.event_id):
                                #     o_line.product_uom_qty = len(o_line.event_id)
                            if o_line_danger.is_inactive:
                                o_line.is_inactive = True
                                o_line.is_duplicate = False
                                # if len(line.event_id) < len(o_line.event_id):
                                #     o_line.product_uom_qty = len(o_line.event_id)



    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        if not self.sale_order_template_id:
            self.require_signature = self._get_default_require_signature()
            self.require_payment = self._get_default_require_payment()
            return
        template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)

        order_lines = []
        if not self.order_line:
            custom_sequence_new = 0
        if self.order_line:
            custom_sequence_new = self.order_line[-1].custom_sequence_new
        for line in template.sale_order_template_line_ids:
            data = self._compute_line_data_for_template_change(line)
            if line.product_id:
                discount = 0
                if self.pricelist_id:
                    price = self.pricelist_id.with_context(uom=line.product_uom_id.id).get_product_price(line.product_id, 1, False)
                    if self.pricelist_id.discount_policy == 'without_discount' and line.price_unit:
                        discount = (line.price_unit - price) / line.price_unit * 100
                        # negative discounts (= surcharge) are included in the display price
                        if discount < 0:
                            discount = 0
                        else:
                            price = line.price_unit
                    elif line.price_unit:
                        price = line.price_unit

                else:
                    price = line.price_unit

                data.update({
                    'price_unit': price,
                    'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                    'product_uom_qty': line.product_uom_qty,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom_id.id,
                    'custom_sequence_new': custom_sequence_new + 1 or 0,
                    'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                })
                if self.pricelist_id:
                    data.update(self.env['sale.order.line']._get_purchase_price(self.pricelist_id, line.product_id, line.product_uom_id, fields.Date.context_today(self)))
            order_lines.append((0, 0, data))
        self.order_line = order_lines
        self.order_line._compute_tax_id()
        option_lines = []
        for option in template.sale_order_template_option_ids:
            data = self._compute_option_data_for_template_change(option)
            option_lines.append((0, 0, data))
        self.sale_order_option_ids = option_lines

        if template.number_of_days > 0:
            self.validity_date = fields.Date.to_string(datetime.now() + timedelta(template.number_of_days))

        self.require_signature = template.require_signature
        self.require_payment = template.require_payment

        if template.note:
            self.note = template.note

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_duplicate = fields.Boolean(string="Duplicate")
    is_inactive = fields.Boolean('Set as Inactive')
    custom_sequence_new = fields.Integer(string="Sequence", store=True)
    display_type = fields.Selection(selection_add=[('q_temp', 'Quotation Template')])
    sale_order_template_id = fields.Many2one(
        'sale.order.template', 'Quotation Template',
        check_company=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    is_master_event = fields.Boolean(string="Master Event", store=True)
    event_id = fields.One2many('project.event', 'sale_order_line_ids', string="Events")
    color = fields.Char(string="Color",store=True)

    @api.model
    def create(self, vals):
        if 'event_id' in vals and 'product_uom_qty' in vals:
            master_data = {}
            master_event_lines = []
            if vals['product_uom_qty'] == 1:
                master_data = {
                    'custom_sequence': 0,
                    'name': 'Event 1',
                    'from_date': vals['event_id'][0][2]['from_date'],
                    'to_date': vals['event_id'][0][2]['to_date'],
                    'product_id': vals['product_id']
                }
                master_event_lines.append((0, 0, master_data))
                vals['event_id'] = master_event_lines
        elif 'product_uom_qty' in vals:
            master_data = {}
            master_event_lines = []
            if vals['product_uom_qty'] == 1:
                master_data = {
                    'custom_sequence': 0,
                    'name': 'Event 1',
                    'from_date': datetime.now().date(),
                    'to_date': datetime.now().date(),
                    'product_id': vals['product_id']
                }
                master_event_lines.append((0, 0, master_data))
                vals['event_id'] = master_event_lines
        result = super(SaleOrderLine, self).create(vals)
        return result

    @api.onchange('product_uom_qty')
    def orderline_qty(self):
        event_lines = []
        data = {}

        # if self.product_id.is_master_event:
        updated_qty = self.product_uom_qty
        updated_qty = int(updated_qty)

        '''While changing the qty for the Main Event restrict 
        if the Qty enetred is less than Events Len '''

        if updated_qty < len(self.event_id):
            qtys = len(self.event_id)
            self.product_uom_qty = qtys
            return False
        else:
            present_events = len(self.event_id)
            new_line = updated_qty - present_events
            for event in range(new_line):
                data = {
                        'custom_sequence': self.event_id[-1].custom_sequence + event + 1 if self.event_id else False,
                        'name': 'Event %d' % (len(self.event_id) + event + 1),
                        'from_date': datetime.now().date(),
                        'to_date': datetime.now().date(),
                        'product_id': self.product_id.id,
                }
                event_lines.append((0, 0, data))

            #Assign Events and dates
            self.event_id = event_lines

    @api.onchange('event_id')
    def remove_event(self):
        if len(self.event_id) == 0:
            raise UserError(_("Minimum 1 record Should Exists"))
        self.product_uom_qty = len(self.event_id)

    @api.model
    def default_get(self, fields):
        res = super(SaleOrderLine, self).default_get(fields)
        res['is_master_event'] = self.product_id.is_master_event
        if self.is_master_event:
            if self.product_uom_qty != len(self.event_id):
                master_data = {}
                master_event_lines = []
                if self.product_uom_qty == 1:
                    master_data = {
                        'custom_sequence': 0,
                        'name': 'Event %d' % (len(self.event_id) + 1),
                        'from_date': datetime.now().date(),
                        'to_date': datetime.now().date(),
                        'product_id': self.product_id.id
                    }
                    master_event_lines.append((0, 0, master_data))
                    # Assign Events and dates
                res['event_id'] = master_event_lines
        return res

    @api.depends('product_id')
    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        self.is_master_event = self.product_id.is_master_event
        return res
