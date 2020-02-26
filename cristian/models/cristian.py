from odoo import fields, models, api

class ContractCristian(models.Model):

    _inherit = 'hr.contract'
    _description = 'Campos nuevos para el contrato'

    arl = fields.Many2one('res.partner',string="ARL")

    eps = fields.Many2one('res.partner',string="EPS")

    pension = fields.Many2one('res.partner',string="Pensión")

    cesantias = fields.Many2one('res.partner',string="Cesantias")

    caja = fields.Many2one('res.partner', string="Caja de compensación familiar")

    