# -*- coding: utf-8 -*-

from odoo import models, fields


class EventModule(models.Model):

    _name = 'product.eventmodule'
    _description = 'Eventmodule'
    _rec_name = 'description_intern'

    product_id = fields.Many2one('product.product')
    description_intern = fields.Char('Description Intern')
    description_extern = fields.Char('Description Extern')
    product_employee = fields.Char('Employee')
    text_intern = fields.Text('Text Intern')
    text_extern = fields.Text('Text Extern')
    product_ids = fields.Many2many('product.product', string="Event Products")
    attachment_ids = fields.One2many('ir.attachment', 'res_id',
                                     domain=[('res_model', '=', 'product.eventmodule')],
                                     string='Attachments')
    is_auto = fields.Boolean('Auto')
    to_press = fields.Boolean('To press')
    is_parts_locked = fields.Boolean('Parts locked')
    is_visible = fields.Boolean('Visible')
    is_revision_completed = fields.Boolean('Revision Completed')
    is_briefing_available = fields.Boolean('Briefing Available')
    checklist_ids = fields.Many2many('event.checklist', string='Checklist')
    checklist_number = fields.Char('Number')
    skill_ids = fields.Many2many('tech.tech', string='Skills')
    image_1920 = fields.Image("Image")
    lst_price = fields.Float('Public Price')
