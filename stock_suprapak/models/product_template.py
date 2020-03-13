# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit  = 'product.template'

    x_currency_id = fields.Many2one('res.currency', 'Currency')
    customer_reference = fields.Char('Customer Reference')
    version = fields.Char('Version')
    date_version = fields.Date('Date Version')
    class_print = fields.Char('Class of Print')
    presentation = fields.Char('Presentation')
    type_selle = fields.Char('Type of Sealed')
