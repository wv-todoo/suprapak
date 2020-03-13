# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DataSheet(models.Model):
    _name = 'data.sheet'
    _description = 'Data sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company.id)
    opportunity_id = fields.Many2one('crm.lead', 'Opportunity')
    state = fields.Selection([('draft', 'Quote sheet'), ('sample', 'Sample Tab'),
                              ('order', 'Order Tab')],
                             'state', copy=False, default='draft')
    type_sheet = fields.Selection([('review', 'Review'), ('technical', 'Technical Approval'), ('design', 'Design approval'),
                                   ('approved','Approved'),('rejected','Rejected'),('obsolete','Obsolete'),
                                   ('rejected ','Rejected Technical '),('rejected_d','Rejected Design')], 'Type sheet')
    name = fields.Char('Name')
    product_id = fields.Many2one('product.product', 'Product')
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], 'Priority')
    # Info Customer
    partner_id = fields.Many2one('res.partner', 'Customer')
    commentary = fields.Char('Commentary')
    product_code = fields.Char('Product code', help='Customer product code')
    team_id = fields.Many2one('crm.team', 'Zone')
    currency_id = fields.Many2one('res.currency', 'Currency')

    # Info Tec
    print_class = fields.Selection([('external','External'),('internal','Internal')],'Print Class')
    print_type = fields.Many2one('print.type','Print Type')
    uom_id = fields.Many2one('uom.uom', 'Unit of measure')
    product_type_id = fields.Many2one('data.product.type', 'Product line')
    draw_type_id = fields.Many2one('data.draw.type', 'Draw type')
    movie_type_id = fields.Many2one('data.movie.type', 'Movie type')
    color_movie__id = fields.Many2one('data.movie.color', 'Color movie')
    chemical_composition = fields.Many2one('chemical.composition','Chemical Composition')
    # Info cant
    specification_width_id = fields.Many2one('specification.width','Specification width')
    specification_long_id = fields.Many2one('specification.long','Specification long')
    caliber_id = fields.Many2one('data.caliber.type', 'Specification caliber')
    tolerance_width = fields.Integer('Tolerance width')
    tolerance_long = fields.Integer('Tolerance long')
    tolerance_caliber = fields.Integer('Tolerance caliber')
    # Bool
    tongue = fields.Boolean('Tongue')
    thermal_adhesive = fields.Boolean('Thermal adhesive')
    print = fields.Boolean('Print')
    no_print = fields.Boolean('Without Print')
    rhombus = fields.Boolean('Rhombus')
    guillotine = fields.Boolean('Requires Guillotine')
    guillotine = fields.Boolean('')

    # Comments
    comments = fields.Text('Comments')
    # Button
    quotation_count = fields.Integer(compute='_compute_sale_data', string="Number of Quotations")
    order_ids = fields.One2many('sale.order', 'sheet_id', string='Orders')
    photo = fields.Binary()
    tag_form_id = fields.Many2one('data.tag.form','Tag Form')
    material_id = fields.Many2one('data.material','Material')
    application_id = fields.Many2one('data.application.mode','Application Mode')
    position_id = fields.Many2one('data.application.position','Application Position')
    content_id = fields.Many2one('data.application.contents','Package Contents')
    quantity = fields.Char('Quantity')
    form_id = fields.Many2one('data.form','Form')
    overlap_id = fields.Many2one('Width.overlap','Width Overlap')
    tolerance = fields.Char('Tolerance')
    overlap_location_id = fields.Many2one('overlap.location','Overlap Location')
    list_id = fields.Many2one('mrp.bom')
    lists_ids = fields.Many2many('mrp.bom','sheet_bom_rel','sheet_id','bom_id','Bills of Materials')
    routing_id = fields.Many2one('mrp.routing','Routings')
    routings_ids = fields.Many2many('mrp.routing','sheet_routing_rel','sheet_id','routing_id','Routing')

    @api.onchange('overlap_id')
    def _onchange_overlap_id(self):
        if self.overlap_id:
            self.tolerance = self.overlap_id.tolerance


    def _compute_sale_data(self):
        for lead in self:
            lead.quotation_count = len(lead.order_ids)

    @api.onchange('movie_type_id')
    def _onchange_movie_type_id(self):
        if self.movie_type_id:
            self.color_movie__id = self.movie_type_id.color_id

    @api.onchange('caliber_id')
    def _onchange_caliber_id(self):
        if self.caliber_id:
            self.tolerance_caliber = self.caliber_id.tolerance

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id

    def write(self, values):
        res = super(DataSheet, self).write(values)
        self.action_create_quotation()
        return res

    def action_create_quotation(self):
        so_obj = self.env['sale.order']
        for record in self:
            if not record.partner_id:
                raise ValidationError("Por favor asignar un cliente")
            vals = {
                'product_id': record.product_id.id,
                'product_uom': record.uom_id.id,
                'product_type_id': record.product_type_id.id,
                'draw_type_id': record.draw_type_id.id,
                'movie_type_id': record.movie_type_id.id,
<<<<<<< HEAD
                'specification_width': record.specification_width_id.id,
                'specification_long': record.specification_long_id.id,
=======
                'specification_width': record.specification_width.id,
                'specification_long': record.specification_long.id,
>>>>>>> origin/staging3
                'caliber_id': record.caliber_id.id,
                'tongue': record.tongue,
                'thermal_adhesive': record.thermal_adhesive,
            }
            val = {
                'opportunity_id': record.opportunity_id.id if record.opportunity_id else None,
                'partner_id': record.partner_id.id,
                'origin': record.name,
                'company_id': self.company_id.id or self.env.company.id,
                'sheet_id': record.id,
                'order_line': [(0, 0, vals)],
            }
            so = so_obj.create(val)
            so.order_line.product_id_change()

    def action_sale_quotations_new(self):
        '''if not self.partner_id:
            return self.env.ref("sale_crm.crm_quotation_partner_action").read()[0]
        else:
            return self.action_new_quotation()'''
        self.action_create_quotation()

    def action_new_quotation(self):
        action = self.env.ref("sale_crm.sale_action_quotations_new").read()[0]
        vals = {
            'product_id': self.product_id.id,
            'product_uom': self.uom_id.id,
            'product_type_id': self.product_type_id.id,
            'draw_type_id': self.draw_type_id.id,
            'movie_type_id': self.movie_type_id.id,
<<<<<<< HEAD
            'specification_width': self.specification_width_id.id,
            'specification_long': self.specification_long_id.id,
=======
            'specification_width': self.specification_width.id,
            'specification_long': self.specification_long.id,
>>>>>>> origin/staging3
            'caliber_id': self.caliber_id.id,
        }
        action['context'] = {
            'search_default_opportunity_id': self.opportunity_id.id,
            'default_opportunity_id': self.opportunity_id.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_origin': self.name,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_sheet_id': self.id,
            'default_order_line': [(0, 0, vals)],
        }
        return action

    def action_view_sale_quotation(self):
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        action['context'] = {
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_sheet_id': self.id
        }
        action['domain'] = [('sheet_id', '=', self.id)]
        quotations = self.mapped('order_ids')
        if len(quotations) == 1:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = quotations.id
        return action


class DataProductType(models.Model):
    _name = 'data.product.type'
    _description = 'Product type'

    name = fields.Char('Name')
    code = fields.Char('Code')


class DataDrawType(models.Model):
    _name = 'data.draw.type'
    _description = 'Drawing type'

    name = fields.Char('Name')
    code = fields.Char('Code')


class DataMovieColor(models.Model):
    _name = 'data.movie.color'
    _description = 'Movie color'

    name = fields.Char('Name')
    code = fields.Char('Code')


class DataMovieType(models.Model):
    _name = 'data.movie.type'
    _description = 'Movie type'

    name = fields.Char('Name')
    code = fields.Char('Code')
    color_id = fields.Many2one('data.movie.color', 'Color')


class DataCaliberType(models.Model):
    _name = 'data.caliber.type'
    _description = 'Caliber type'

    name = fields.Char('Name')
    code = fields.Char('Code')
    tolerance = fields.Integer('Tolerance')

class DataForm(models.Model):
    _name = 'data.form'
    _description = 'Form'

    name = fields.Char('Form')
    code = fields.Char('code')

class DataTagForm(models.Model):
    _name = 'data.tag.form'
    _description = 'Tag Form'

    name = fields.Char('Tag Form')
    code = fields.Char('code')

class DataMaterial(models.Model):
    _name = 'data.material'
    _description = 'Material'

    name = fields.Char('Material')
    code = fields.Char('code')

class DataAplication(models.Model):
    _name = 'data.application.mode'
    _description = 'Aplication Mode'

    name = fields.Char('Application Mode')
    code = fields.Char('code')

class DataAplication(models.Model):
    _name = 'data.application.position'
    _description = 'Application Position'

    name = fields.Char('Aplication Position')
    code = fields.Char('code')

class DataContents(models.Model):
    _name = 'data.application.contents'
    _description = 'Package Contents'

    name = fields.Char('Package Contents')
    code = fields.Char('code')

class PrintType(models.Model):
    _name = 'print.type'
    _description = 'Print Type'

    name = fields.Char('Print Type')
    code = fields.Char('code')


class ChemicalComposition(models.Model):
    _name = 'chemical.composition'
    _description = 'Chemical Composition'

    name = fields.Char('Chemical Composition')
    code = fields.Char('code')

class SpecificationWidth(models.Model):
    _name = 'specification.width'
    _description = 'Specification Width'

    name = fields.Char('Specification Width')
    code = fields.Char('code')

class SpecificationLong(models.Model):
    _name = 'specification.long'
    _description = 'Specification Long'

    name = fields.Char('Specification Long')
    code = fields.Char('code')

class Widthoverlap(models.Model):
    _name = 'width.overlap'
    _description = 'Width Overlap'

    name = fields.Char('Width Overlap')
    tolerance = fields.Char('Tolerance')
    code = fields.Char('code')
<<<<<<< HEAD

class Widthoverlap(models.Model):
    _name = 'overlap.location'
    _description = 'Overlap Location'

    name = fields.Char('Overlap Location')
    code = fields.Char('code')
=======
>>>>>>> origin/staging3
