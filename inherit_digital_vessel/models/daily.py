from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta

class Vessel_activity_line(models.Model):
    _name ='vessel.activity.line'
    
    activity = fields.Selection([
        ('to Dum area priok', 'to Dum area priok'),
        ('Tiba di Alur', 'Tiba di Alur'),
        ('Break/Stop', 'Break/Stop'),
        ('Start Ops', 'Start Ops'),
        ('Kembali ke pangkalan', 'Kembali ke pangkalan'),
        ], string='Activity')
    time =fields.Float(string="Time/Jam")
    daily_id = fields.Many2one('daily.ops', string="Daily id", required=True, ondelete="cascade")

class Daily(models.Model):
    _name = 'daily.ops'
    
    name = fields.Char(string="Daily Ops Number", readonly=True, required=True, copy=False, default='New')
    report_date =fields.Datetime(string="Report Date", required=True)
    vessel_id = fields.Many2one('vessel.vessel', string="Nama Kapal", required=True)
    note = fields.Text(string="Catatan")
    captain_id = fields.Many2one('hr.employee', string="Captain", required=True)
    approved_by = fields.Many2one('hr.employee', string="Approved By")
    prepared_by = fields.Many2one('hr.employee', string="Prepared By", required=True)
    location_id = fields.Many2one('location.location', string="Location", required=True)
    working_area_id = fields.Many2one('working.area', string="Working Area", required=True)
    cuaca = fields.Selection([
        ('Hujan', 'Hujan'),
        ('Badai', 'Badai'),
        ('Cerah', 'Cerah'),
        ('Berawan', 'Berawan'),
        ], string='Cuaca', required=True)

    status = fields.Selection([
        ('Operation', 'Operation'),
    	('Stand By', 'Stand By'),
    	('Breakdown', 'Breakdown'),
        ('Preventive Maintenance', 'Preventive Maintenance'),
        ], string='Status', required=True)

    stage = fields.Selection([
        ('Waiting', 'Waiting'),
        ('Approved', 'Approved'),
        ('Reject', 'Reject')
        ], string='Sign', default="Waiting")

    op_start = fields.Float(string="Operation Start")
    op_finish = fields.Float(string="Operation Finish")
    stop_op = fields.Float(string="Stop Operation")
    total_op = fields.Float(string="Total Operation", readonly=True, compute="_compute_total_op")

    # rob_awal =fields.Float(string="ROB Awal", default=0)
    # rob_pemakaian =fields.Float(string="Pemakaian", default=0)
    # rob_akhir = fields.Float(string="ROB Akhir", compute="_compute_rob_akhir")
    rob_awal =fields.Float(string="ROB Awal", default=0)
    rob_pemakaian =fields.Float(string="Pemakaian", compute="_compute_rob_pemakaian")
    rob_akhir = fields.Float(string="ROB Akhir", default=0)

    x_css = fields.Html(string='CSS', sanitize=False, store=False, compute='_compute_css')

    vessel_activity_line_ids = fields.One2many('vessel.activity.line', 'daily_id',  string="Vessel Activity")

    # kamar_mesin_line_ids = fields.One2many('kamar.mesin.line', 'weekely_id',  string="Description")
    # deck_line_ids = fields.One2many('deck.line', 'weekely_id',  string="Deck")
    # wheel_house_ids = fields.One2many('wheel.house.line', 'weekely_id',  string="Wheel House")

    @api.depends('stage')
    def _compute_css(self):
        for rec in self:
            # Modify below condition
            if rec.stage == 'Approved' or rec.stage == 'Reject':
                rec.x_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                rec.x_css = False

    @api.depends('op_start', 'op_finish', 'stop_op')
    def _compute_total_op(self):

        for rec in self:
            rec.total_op = rec.op_finish - rec.op_start - rec.stop_op
    
    # @api.depends('rob_awal', 'rob_pemakaian')
    # def _compute_rob_akhir(self):

    #     for rec in self:
    #         if rec.rob_awal and rec.rob_pemakaian:
    #             rob_akhir = rec.rob_awal - rec.rob_pemakaian
    #             rec.rob_akhir = rob_akhir
    @api.depends('rob_awal', 'rob_akhir')
    def _compute_rob_pemakaian(self):

        for rec in self:
            if rec.rob_awal and rec.rob_akhir:
                rob_pemakaian = rec.rob_awal - rec.rob_akhir
                rec.rob_pemakaian = rob_pemakaian

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('self.daily') or 'New'
        result = super(Daily, self).create(vals)
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
