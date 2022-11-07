from odoo import fields, models, api, _

class ResPartner(models.Model):
    _inherit = "res.partner"

    customer = fields.Boolean(string='Is a Customer')
    supplier = fields.Boolean(string='Is a Supplier')
