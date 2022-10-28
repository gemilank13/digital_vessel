from odoo import models, fields, api

class Dashboard_vessel(models.Model):
    _name = 'dashboard.vessel'

    vessel_id = fields.Many2one('vessel.vessel', string="Nama Kapal")
    status = fields.Selection([
        ('Operation', 'Operation'),
    	('Stand By', 'Stand By'),
    	('Breakdown', 'Breakdown'),
    	('Docking', 'Docking'),
        ('Preventive Maintenance', 'Preventive Maintenance'),
        ('Corrective Maintenance', 'Corrective Maintenance')
        ], string='Status')
        
    date = fields.Datetime(string="Date")