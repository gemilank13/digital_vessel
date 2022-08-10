from odoo import models, fields, api

class Kamarmesinline(models.Model):

    _name = 'kamar.mesin.line'

    kamarmesin_id = fields.Many2one('kamar.mesin', string="Description", required=True)
    status = fields.Selection([
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor')
        ], string='Condition', required=True)
    remark = fields.Text(string="remark")
    
    weekely_id = fields.Many2one('weekly.inspection', string='Weekely Id')

class DeckWeeklyline(models.Model):

    _name = 'deck.line'
    
    deck_id = fields.Many2one('deck.deck', string="Description", required=True)
    status = fields.Selection([
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor')
        ], string='Condition', required=True)
    remark = fields.Text(string="remark")
    
    weekely_id = fields.Many2one('weekly.inspection', string='Weekely Id')

class Wheelhouseline(models.Model):

    _name = 'wheel.house.line'
    
    wheelhouse_id = fields.Many2one('wheel.house', string="Description", required=True)
    status = fields.Selection([
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor')
        ], string='Condition', required=True)
    remark = fields.Text(string="remark")
    
    weekely_id = fields.Many2one('weekly.inspection', string='Weekely Id')


class Weekly(models.Model):
    _name = 'weekly.inspection'
    
    name = fields.Char(string="Weekly Inspeksi Number", readonly=True, required=True, copy=False, default='New')
    start_date =fields.Datetime(string="Check Date Time", required=True)
    vessel_id = fields.Many2one('vessel.vessel', string="Nama Kapal", required=True)
    checked_by = fields.Many2one('hr.employee', string="Checked By", required=True)
    approved_by = fields.Many2one('hr.employee', string="Mengetahui")
    prepared_by = fields.Many2one('hr.employee', string="Pelaksana", required=True)
    r_h_hours = fields.Char(string="R/H (Hours)")

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

    kamar_mesin_line_ids = fields.One2many('kamar.mesin.line', 'weekely_id',  string="Kamar Mesin")
    deck_line_ids = fields.One2many('deck.line', 'weekely_id',  string="Deck")
    wheel_house_ids = fields.One2many('wheel.house.line', 'weekely_id',  string="Wheel House")

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'stage': 'Approved'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'stage': 'Reject'})
