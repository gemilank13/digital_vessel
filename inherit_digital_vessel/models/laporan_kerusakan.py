from odoo import models, fields, api

class Kerusakanline(models.Model):

    _name = 'kondisi.kerusakan.line'

    name = fields.Text(string="Deskripsi")
    photos = fields.Binary(string="Foto", required=True)
    kerusakan_id = fields.Many2one('laporan.kerusakan', string='laporan kerusakan Id')

class Permintaanrepair(models.Model):

    _name = 'permintaan.repair.line'

    name = fields.Text(string="Deskripsi")
    photos = fields.Binary(string="Foto", required=True)
    kerusakan_id = fields.Many2one('laporan.kerusakan', string='laporan kerusakan Id')

class Laporankerusakan(models.Model):
    _name = 'laporan.kerusakan'
    
    name = fields.Char(string="Nomor Laporan", readonly=True, required=True, copy=False, default='New')
    vessel_id = fields.Many2one('vessel.vessel', string="Nama Kapal", required=True)
    location_id = fields.Many2one('location.location', string="Lokasi")
    datetime = fields.Datetime(string="Tanggal/Jam")
    kerusakan = fields.Char(string="Kerusakan Pada")
    crew_id = fields.Many2one('hr.employee', string="Crew")
    approved_by = fields.Many2one('hr.employee', string="Mengetahui")
    prepared_by = fields.Many2one('hr.employee', string="Pelaksana")
    r_h_hours = fields.Char(string="R/H (Hours)")
    status = fields.Selection([
        ('Operation', 'Operation'),
        ('Stand By', 'Stand By'),
        ('Breakdown', 'Breakdown')
        ], string='Status', required=True)

    repair = fields.Selection([
        ('Permanent', 'Permanent'),
        ('Temporary', 'Temporary')
        ], string='Repair', required=True)

    permintaan_repair = fields.Selection([
        ('Urgent', 'Urgent'),
        ('Waktu Dock', 'Waktu Dock'),
        ('Selama 1 Bulan', 'Selama 1 Bulan')
        ], string='Permintaan Repair', required=True)

    stage = fields.Selection([
        ('Waiting', 'Waiting'),
        ('Approved', 'Approved'),
        ('Reject', 'Reject')
        ], string='Sign', default="Waiting")

    kerusakan_line_ids = fields.One2many('kondisi.kerusakan.line', 'kerusakan_id',  string="Kondisi Kerusakan")
    permintaan_line_ids = fields.One2many('permintaan.repair.line', 'kerusakan_id',  string="Permintaan Repair")
    # deskripsi = fields.Text(string="Deskripsi")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('self.kerusakan') or 'New'
        result = super(Laporankerusakan, self).create(vals)
        return result


    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'stage': 'Approved'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'stage': 'Reject'})