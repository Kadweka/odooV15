# -*- coding: utf-8 -*-

from odoo import models, fields


class HeExpense(models.Model):
    _inherit = 'hr.expense'

    ref = fields.Char(string='Ref')
    sendto_uid = fields.Many2one('hr.employee', string='Responsible Approver')
