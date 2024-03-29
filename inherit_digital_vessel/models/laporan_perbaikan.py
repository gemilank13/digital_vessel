from odoo import models, fields, api

class Tahapperbaikan(models.Model):

    _name = 'tahap.perbaikan.line'

    name = fields.Text(string="Deskripsi", required=True)
    photos = fields.Binary(string="Foto", required=False)
    perbaikan_id = fields.Many2one('laporan.perbaikan', string='laporan perbaikan Id')

class Tahappemeriksaanfisik(models.Model):

    _name = 'tahap.pemeriksaan.fisik.line'

    name = fields.Text(string="Deskripsi", required=True)
    photos = fields.Binary(string="Foto", required=False)
    perbaikan_id = fields.Many2one('laporan.perbaikan', string='laporan perbaikan Id')


class Sparepart(models.Model):

    _name = 'sparepart.line'

    name = fields.Text(string="Deskripsi", required=True)
    photos = fields.Binary(string="Foto", required=False)
    perbaikan_id = fields.Many2one('laporan.perbaikan', string='laporan perbaikan Id')


class Laporanperbaikan(models.Model):
    _name = 'laporan.perbaikan'
    
    name = fields.Char(string="Nomor Laporan", readonly=True, required=True, copy=False, default='New')
    vessel_id = fields.Many2one('vessel.vessel', string="Nama Kapal", required=True, compute='_compute_kerusakan')
    location_id = fields.Many2one('location.location', string="Lokasi")
    datetime = fields.Datetime(string="Tanggal/Jam")
    kerusakan_id = fields.Many2one('laporan.kerusakan', string="No. Laporan Kerusakan")
    perbaikan = fields.Char(string="Perbaikan Pada", readonly=True, compute='_compute_kerusakan')
    tgl_kerusakan = fields.Datetime(string="Tanggal Kerusakan", readonly=True, compute='_compute_kerusakan')
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
    x_css = fields.Html(string='CSS', sanitize=False, compute='_compute_css', store=False)

    @api.depends('stage')
    def _compute_css(self):
        for rec in self:
            # Modify below condition
            if rec.stage == 'Approved' or rec.stage=='Reject':
                rec.x_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                rec.x_css = False
                
    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'stage': 'Approved'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'stage': 'Reject'})
    
    @api.depends('kerusakan_id') #ok
    def _compute_kerusakan(self):
        for laporan in self:
            if laporan.kerusakan_id:
                laporan.vessel_id =laporan.kerusakan_id.vessel_id.id
                # laporan.location_id = laporan.kerusakan_id.location_id.id
                laporan.perbaikan= laporan.kerusakan_id.kerusakan
                laporan.tgl_kerusakan = laporan.kerusakan_id.datetime

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('self.perbaikan') or 'New'
        result = super(Laporanperbaikan, self).create(vals)
        return result