from odoo import models, fields, api

class Tahapperbaikan(models.Model):

    _name = 'tahap.perbaikan.line'

    name = fields.Text(string="Deskripsi")
    photos = fields.Binary(string="Foto")
    perbaikan_id = fields.Many2one('laporan.perbaikan', string='laporan perbaikan Id')

class Tahappemeriksaanfisik(models.Model):

    _name = 'tahap.pemeriksaan.fisik.line'

    name = fields.Text(string="Deskripsi")
    photos = fields.Binary(string="Foto")
    perbaikan_id = fields.Many2one('laporan.perbaikan', string='laporan perbaikan Id')


class Sparepart(models.Model):

    _name = 'sparepart.line'

    name = fields.Text(string="Deskripsi")
    photos = fields.Binary(string="Foto")
    perbaikan_id = fields.Many2one('laporan.perbaikan', string='laporan perbaikan Id')


class Laporanperbaikan(models.Model):
    _name = 'laporan.perbaikan'
    
    name = fields.Char(string="Nomor Laporan", readonly=True, required=True, copy=False, default='New')
    vessel_id = fields.Many2one('vessel.vessel', string="Nama Kapal", required=True)
    location_id = fields.Many2one('location.location', string="Lokasi")
    datetime = fields.Datetime(string="Tanggal/Jam")
    kerusakan_id = fields.Many2one('laporan.kerusakan', string="No. Laporan Kerusakan")
    perbaikan = fields.Char(string="Perbaikan Pada", readonly=True)
    tgl_kerusakan = fields.Datetime(string="Tanggal Kerusakan", readonly=True)
    crew_id = fields.Many2one('hr.employee', string="Crew")
    approved_by = fields.Many2one('hr.employee', string="Mengetahui")
    prepared_by = fields.Many2one('hr.employee', string="Pelaksana")
    stage = fields.Selection([
        ('Waiting', 'Waiting'),
        ('Approved', 'Approved'),
        ('Reject', 'Reject')
        ], string='Sign', default="Waiting")

    tahap_perbaikan_line_ids = fields.One2many('tahap.perbaikan.line', 'perbaikan_id',  string="Tahap Perbaikan")
    tahap_pemeriksaan_line_ids = fields.One2many('tahap.pemeriksaan.fisik.line', 'perbaikan_id',  string="Tahap Pemeriksaan Fisik & Penyelesaian Pengujian")
    sparepart_line_ids = fields.One2many('sparepart.line', 'perbaikan_id',  string="Spare Part Diganti")

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'stage': 'Approved'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'stage': 'Reject'})
    
    @api.onchange('kerusakan_id') #ok
    def _onchange_kerusakan(self):
        for laporan in self:
            if laporan.kerusakan_id:
                laporan.perbaikan= laporan.kerusakan_id.kerusakan
                laporan.tgl_kerusakan = laporan.kerusakan_id.datetime

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('self.perbaikan') or 'New'
        result = super(Laporanperbaikan, self).create(vals)
        return result