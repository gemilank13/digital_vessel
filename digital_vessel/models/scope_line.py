# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ScopeLine(models.Model):
    _name = 'scope.line'
    
    scope_id = fields.Many2one('scope.scope', string="Scope", required=True)
    pm_id = fields.Many2one('preventive.maintenance', string='PM Id')
    repair_id = fields.Many2one('repair.order', string='repair Id')