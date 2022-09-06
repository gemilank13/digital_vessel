from odoo import models, fields, api

class Minjobline(models.Model):

    _name = 'min.job.line'

    name = fields.Text(string="Deskripsi")
    docking_id = fields.Many2one('docking.docking', string='Docking Id')

class Addjobline(models.Model):

    _name = 'add.job.line'

    name = fields.Text(string="Deskripsi")
    docking_id = fields.Many2one('docking.docking', string='Docking Id')

class inheritcomponendocking(models.Model):
    _inherit = 'component.line'

    vendor = fields.Char(string='Vendor')
    spec_id = fields.Many2one('dock.dock', string="Spec", required=True)
    docking_id = fields.Many2one('docking.docking', string='Docking Id')

class inheritscopelinedocking(models.Model):
    _inherit = 'scope.line'

    docking_id = fields.Many2one('docking.docking', string='Docking Id')

class Docking(models.Model):
    _name = 'docking.docking'
    
    name = fields.Char(string="Docking Report Number", readonly=True, required=True, copy=False, default='New')
    start_date =fields.Datetime(string="Start Date")
    finish_date = fields.Datetime(string="Finish Date")
    vessel_id = fields.Many2one('vessel.vessel', string="Nama Kapal", required=True)
    dock_id = fields.Many2one('dock.dock', string="Dock", required=True)
    customer_id = fields.Many2one('customer.customer', string="Customer")
    location_id = fields.Many2one('location.location', string="Lokasi")
    approved_by = fields.Many2one('hr.employee', string="Prepared By")
    prepared_by = fields.Many2one('hr.employee', string="Approved By")
    jobcode_id = fields.Many2one('job.code', string="Job Code")
    pic_id = fields.Many2one('hr.employee', string="PIC")
    r_h_hours = fields.Char(string="R/H (Hours)")
    remarks = fields.Text(string="Remarks")
    progress = fields.Char(string="Progress Presentasi (%)")

    status = fields.Selection([
        ('Operation', 'Operation'),
    	('Stand By', 'Stand By'),
    	('Breakdown', 'Breakdown'),
    	('Docking', 'Docking'),
        ('Preventive Maintenance', 'Preventive Maintenance'),
        ('Corrective Maintenance', 'Corrective Maintenance')
        ], string='Status', required=True)

   
    stage = fields.Selection([
        ('Waiting', 'Waiting'),
        ('Approved', 'Approved'),
        ('Reject', 'Reject')
        ], string='Sign', default="Waiting")

    scope_line_ids = fields.One2many('scope.line', 'docking_id',  string="Scope Line")
    componen_line_ids = fields.One2many('component.line', 'docking_id',  string="Dock Line")
    add_job_line_ids = fields.One2many('add.job.line', 'docking_id',  string="Add Job")
    min_job_line_ids = fields.One2many('min.job.line', 'docking_id',  string="Min Job")
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
            vals['name'] = self.env['ir.sequence'].next_by_code('self.docking') or 'New'
        result = super(Docking, self).create(vals)
        return result

    @api.multi
    def button_approved(self):
        for rec in self:
            rec.write({'stage': 'Approved'})

    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'stage': 'Reject'})
