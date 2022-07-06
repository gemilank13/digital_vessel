# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ComponentLine(models.Model):
    _name = 'component.line'
    
    component_id = fields.Many2one('component.component', string="Part/Component", required=True)
    qty = fields.Integer(string="Qty", required=True)
    unit_id = fields.Many2one('uom.uom', string="Unit", required=True)
    photos = fields.Binary(string="Photos")
    keterangan = fields.Char(string="Keterangan")
    pm_id = fields.Many2one('preventive.maintenance', string='PM Id')
    repair_id = fields.Many2one('repair.order', string='repair Id')