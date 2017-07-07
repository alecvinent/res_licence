# -*- coding: utf-8 -*-
from openerp import http

# class Utiles(http.Controller):
#     @http.route('/utiles/utiles/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/utiles/utiles/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('utiles.listing', {
#             'root': '/utiles/utiles',
#             'objects': http.request.env['utiles.utiles'].search([]),
#         })

#     @http.route('/utiles/utiles/objects/<model("utiles.utiles"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('utiles.object', {
#             'object': obj
#         })