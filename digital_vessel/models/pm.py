# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import os
import hashlib
import pytz

class PreventiveMaintenance(models.Model):
    _name = 'preventive.maintenance'

    name = fields.Char(string="PM Code", readonly=True, required=True, copy=False, default='New')
    start_date = fields.Datetime(string="Start Date", required=True)
    finish_date = fields.Datetime(string="Finish Date", required=True)
    vessel_id = fields.Many2one('vessel.vessel', string="Nama Kapal", required=True)
    customer_id = fields.Many2one('customer.customer', string="Customer")
    location_id = fields.Many2one('location.location', string="Location")
    pm_period = fields.Selection([('1', '1'),('2', '2'),('3', '3'),('4', '4')], string='PM Period', required=True)
    r_h_hours = fields.Char(string="R/H (Hours)")
    status = fields.Selection([
    	('Operation', 'Operation'),
    	('Stand By', 'Stand By'),
    	], string='Status', required=True)
    sign = fields.Char(string="Sign", readonly=True)
    component_line_ids = fields.One2many('component.line', 'pm_id',  string="Component Line")
    technician_line_ids = fields.One2many('technician.line', 'pm_id',  string="Technician Line")
    scope_line_ids = fields.One2many('scope.line', 'pm_id',  string="Scope Line")
    remarks = fields.Text(string="Remarks")
    approved_by = fields.Many2one('hr.employee', string="Approved By")
    prepared_by = fields.Many2one('hr.employee', string="Prepared By")
    # stage_id = fields.Many2one('stage.stage', 
    #     string='Stage',
    #     track_visibility='onchange')
    stage = fields.Selection([
        ('Waiting', 'Waiting'),
        ('Approved', 'Approved'),
        ('Reject', 'Reject')
        ], string='Stage', default="Waiting")

    x_css = fields.Html(string='CSS', sanitize=False, compute='_compute_css', store=False)
    

    @api.depends('stage')
    def _compute_css(self):
        for rec in self:
            # Modify below condition
            if rec.stage == 'Approved' or rec.stage=='Reject':
                rec.x_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                rec.x_css = False

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('self.name') or 'New'
        result = super(PreventiveMaintenance, self).create(vals)
        return result

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'stage': 'Approved'})

            dashboard_obj = self.env['dashboard.vessel'].search([
                ('vessel_id', '=', rec.vessel_id.id)
            ])

            if dashboard_obj:
                
                dashboard_obj.write({'status': rec.status,
                    'date': rec.create_date
                })

            else:

                vals_dashboard ={
                    'vessel_id': rec.vessel_id.id,
                    'status': rec.status,
                    'date': rec.create_date
                }
                dashboard_obj.create(vals_dashboard)

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'stage': 'Reject'})
