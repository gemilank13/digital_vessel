# -*- coding: utf-8 -*-
from odoo import models, fields, api

class TechnicianLine(models.Model):
    _name = 'technician.line'
    
    technician_id = fields.Many2one('technician.technician', string="Technician", required=True)
    pm_id = fields.Many2one('preventive.maintenance', string='PM Id')
    repair_id = fields.Many2one('repair.order', string='repair Id')