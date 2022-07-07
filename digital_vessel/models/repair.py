# -*- coding: utf-8 -*-
from odoo import models, fields, api

class RepairOrder(models.Model):
    _name = 'repair.order'
    
    name = fields.Char(string="Repair Order Number", readonly=True, required=True, copy=False, default='New')
    start_date = fields.Datetime(string="Start Date", required=True)
    finish_date = fields.Datetime(string="Finish Date", required=True)
    vessel_id = fields.Many2one('vessel.vessel', string="Nama Kapal", required=True)
    customer_id = fields.Many2one('customer.customer', string="Customer")
    location_id = fields.Many2one('location.location', string="Location")
    approved_by = fields.Many2one('hr.employee', string="Approved By")
    prepared_by = fields.Many2one('hr.employee', string="Prepared By")
    r_h_hours = fields.Char(string="R/H (Hours)")
    status = fields.Selection([
        ('Operation', 'Operation'),
        ('Stand By', 'Stand By'),
        ('Breakdown', 'Breakdown'),
        ('Docking', 'Docking')
        ], string='Status', required=True)
    component_line_ids = fields.One2many('component.line', 'repair_id',  string="Component Line")
    technician_line_ids = fields.One2many('technician.line', 'repair_id',  string="Technician Line")
    scope_line_ids = fields.One2many('scope.line', 'repair_id',  string="Scope Line")
    job_code_id = fields.Many2one('job.code', string="Job Code")
    remarks = fields.Text(string="Remarks")
    stage = fields.Selection([
        ('Waiting', 'Waiting'),
        ('Approved', 'Approved'),
        ('Reject', 'Reject')
        ], string='Stage', default="Waiting")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('self.repair') or 'New'
        result = super(RepairOrder, self).create(vals)
        return result

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'stage': 'Approved'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'stage': 'Reject'})

