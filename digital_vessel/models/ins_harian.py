# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime

class InsHarian(models.Model):
    _name = 'ins.harian'
    
    name = fields.Many2one('vessel.vessel', string="Nama Kapal", required=True)
    tgl = fields.Datetime(string="Tanggal & Jam", default=datetime.today())
    status = fields.Selection([
        ('Operation', 'Operation'),
    	('Stand By', 'Stand By'),
    	('Breakdown', 'Breakdown'),
    	('Docking', 'Docking'),
        ('Preventive Maintenance', 'Preventive Maintenance'),
        ('Corrective Maintenance', 'Corrective Maintenance')
        ], string='Status', required=True)