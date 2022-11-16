from odoo import models,fields,_,api,tools

class ResPartner(models.Model):
    
    _inherit = 'res.partner'
    
    gender = fields.Selection([('male','Male'), ('female','Female')],string ="Gender")
