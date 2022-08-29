from odoo import models, fields, api

class Daily(models.Model):
    _name = 'daily.ops'
    
    name = fields.Char(string="Daily Ops Number", readonly=True, required=True, copy=False, default='New')
    report_date =fields.Datetime(string="Report Date", required=True)
    vessel_id = fields.Many2one('vessel.vessel', string="Nama Kapal", required=True)
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
        ('Docking', 'Docking'),
        ('Preventive Maintenance', 'Preventive Maintenance')
        ], string='Status', required=True)

    stage = fields.Selection([
        ('Waiting', 'Waiting'),
        ('Approved', 'Approved'),
        ('Reject', 'Reject')
        ], string='Sign', default="Waiting")

    op_start = fields.Float(string="Operation Start")
    op_finish = fields.Float(string="Operation Finish")
    stop_op = fields.Float(string="Stop Operation")
    total_op = fields.Float(string="Total Operation", readonly=True)

    # kamar_mesin_line_ids = fields.One2many('kamar.mesin.line', 'weekely_id',  string="Description")
    # deck_line_ids = fields.One2many('deck.line', 'weekely_id',  string="Deck")
    # wheel_house_ids = fields.One2many('wheel.house.line', 'weekely_id',  string="Wheel House")


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

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'stage': 'Reject'})
