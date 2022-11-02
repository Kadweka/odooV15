# -*- coding: utf-8 -*-
from dataclasses import field
import string
from odoo import models, fields

class BlockLand(models.Model):
    _name = "land.block"
    _description = "Block Managment model"

    name=fields.Char(string='Name',required=True)
    size=fields.Integer(string='No of Acres',required=True)
    manager=fields.Many2one('res.partner',string='Manager',required=True)
    land_id=fields.Many2one('piece.land',string='Land',required=True)

class BlockSeason(models.Model):
    _name = "block.season"
    _description = "Season Managment Configuration"

    name=fields.Char(string='Name',required=True)
    description=fields.Char(string='Description',required=True)
    crop_id=fields.Many2many('land.block',string='Crop Planted')

class CropBlock(models.Model):
    _name = "crop.block"
    _description = "Crops Managment Configuration"

    name=fields.Char(string='Name',required=True)
    description=fields.Char(string='Description',required=True)
