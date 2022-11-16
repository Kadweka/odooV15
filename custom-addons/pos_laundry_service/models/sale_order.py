from odoo import models, fields, api, _


class LaundryOrder(models.Model):
    _inherit = 'laundry.order'

    sale_note = fields.Text('Note')


class LaundryOrderLine(models.Model):
    _inherit = 'laundry.order.line'

    sale_line_note = fields.Char('Comment')

#     @api.multi
    def _prepare_invoice_line(self, **qty):
        res_id = super(LaundryOrderLine, self)._prepare_invoice_line(**qty)
        if res_id:
            res_id.update({
                           'invoice_line_note' : self.sale_line_note,
                           })
        return res_id
