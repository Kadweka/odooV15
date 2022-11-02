# -*- coding: utf-8 -*-
from dataclasses import field
import string
from typing_extensions import Required
from odoo import models, fields

class PieceLand(models.Model):
    _name = "piece.land"
    _description = "Farm Managment module"

    name=fields.Char(string='Name',required=True)
    size=fields.Integer(string='No of Acres',required=True)
    manager=fields.Many2one('res.partner',string='Manager',required=True)
    block=fields.One2many('land.block','land_id',string='Blocks')