from datetime import timedelta

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval


class StageStage(models.Model):
    _name = 'stage.stage'
    _description = 'Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Stage Name', required=True, translate=True)
    description = fields.Text(translate=True)
    sequence = fields.Integer(default=1)
    # einvoice_ids = fields.One2many('einvoice.t.einvoice', 'einvoice_m_einvoice_stage_id', string='E-Invoice')
    legend_priority = fields.Char(
        string='Starred Explanation', translate=True,
        help='Explanation text to help users using the star on vendor in this stage.')
    legend_blocked = fields.Char(
        'Red Kanban Label', default=lambda s: _('Blocked'), translate=True, required=True,
        help='Override the default value displayed for the blocked state for kanban selection, when the vendor is in that stage.')
    legend_done = fields.Char(
        'Green Kanban Label', default=lambda s: _('Ready for Next Stage'), translate=True, required=True,
        help='Override the default value displayed for the done state for kanban selection, when the vendor is in that stage.')
    legend_normal = fields.Char(
        'Grey Kanban Label', default=lambda s: _('In Progress'), translate=True, required=True,
        help='Override the default value displayed for the normal state for kanban selection, when the vendor is in that stage.')
    # mail_template_id = fields.Many2one(
    #     'mail.template',
    #     string='Email Template',
    #     domain=[('model', '=', 'einvoice.t.einvoice')],
    #     help="If set an email will be sent to the vendor when the task or issue reaches this step.")
    fold = fields.Boolean(string='Folded in Kanban',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')
    # rating_template_id = fields.Many2one(
    #     'mail.template',
    #     string='Rating Email Template',
    #     domain=[('model', '=', 'einvoice.t.einvoice')],
    #     help="If set and if the vendor's rating configuration is 'Rating when changing stage', then an email will be sent to the vendor when the task reaches this step.")
    task_progress = fields.Float('Task Progress (%)', default=0.0)
    is_waiting = fields.Boolean('Is Waiting', default=False)
    is_approved = fields.Boolean('Is Approved', default=False)
    is_not_approved = fields.Boolean('Is Not Approved', default=False)
    sla = fields.Integer('SLA (in Days)')
    # next_stage_ids = fields.Many2many('einvoice.m.einvoice.stage', 'einvoice_next_stage_rel', 'stage_from_id', 'stage_to_id', string='Next Stage')
