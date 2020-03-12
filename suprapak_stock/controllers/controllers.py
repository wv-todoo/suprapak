# -*- coding: utf-8 -*-
# from odoo import http


# class SuprapakStock(http.Controller):
#     @http.route('/suprapak_stock/suprapak_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/suprapak_stock/suprapak_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('suprapak_stock.listing', {
#             'root': '/suprapak_stock/suprapak_stock',
#             'objects': http.request.env['suprapak_stock.suprapak_stock'].search([]),
#         })

#     @http.route('/suprapak_stock/suprapak_stock/objects/<model("suprapak_stock.suprapak_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('suprapak_stock.object', {
#             'object': obj
#         })
