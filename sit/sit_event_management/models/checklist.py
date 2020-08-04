# -*- coding: utf-8 -*-

from odoo import models, fields


class EventChecklist(models.Model):
    _name = 'event.checklist'
    _description = 'Checklist'
    _rec_name = 'name'

    name = fields.Char('name', required="1")
    name_int = fields.Char('Print')
    name_ext = fields.Char('External')
    description = fields.Text('Description')
    is_offer = fields.Boolean('Offer')
    is_event_print = fields.Boolean('Event print')
    is_packlist = fields.Boolean('Packing list')
    is_email_customer = fields.Boolean('Email customer')
    is_mail_MA = fields.Boolean('Mail MA')
    is_mail_event_manager = fields.Boolean('Mail Event Manager')
    is_sms = fields.Boolean('SMS')
    is_module = fields.Boolean('Module')
    is_KIS = fields.Boolean('KIS')
