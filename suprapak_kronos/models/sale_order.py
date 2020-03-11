# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sheet_id = fields.Many2one('data.sheet', 'Sheet')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sheet_id = fields.Many2one('data.sheet', 'Sheet')
    # Info Tec
    product_type_id = fields.Many2one('data.product.type', 'Product type')
    draw_type_id = fields.Many2one('data.draw.type', 'Draw type')
    movie_type_id = fields.Many2one('data.movie.type', 'Movie type')
    # Info cant
    specification_width = fields.Integer('Specification width')
    specification_long = fields.Integer('Specification long')
    caliber_id = fields.Many2one('data.caliber.type', 'Specification caliber')
    # Boolean
    tongue = fields.Boolean('Tongue')
    thermal_adhesive = fields.Boolean('Thermal adhesive')
