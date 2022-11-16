from odoo import api, fields, models, Command, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.http import request, Response
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Description'

    def action_post(self):
        context = self._context
        current_uid = context.get('uid')
        logged_in_user = self.env['res.users'].browse(current_uid)
        #inherit of the function from account.move to validate a new tax and the priceunit of a downpayment
        res = super(AccountMove, self).action_post()
        line_ids = self.mapped('line_ids').filtered(lambda line: line.sale_line_ids.is_downpayment)
        for line in line_ids:
            try:
                line.sale_line_ids.tax_id = line.tax_ids
                if all(line.tax_ids.mapped('price_include')):
                    line.sale_line_ids.price_unit = line.price_unit
                else:
                    #To keep positive amount on the sale order and to have the right price for the invoice
                    #We need the - before our untaxed_amount_to_invoice
                    line.sale_line_ids.price_unit = -line.sale_line_ids.untaxed_amount_to_invoice
            except UserError:
                # a UserError here means the SO was locked, which prevents changing the taxes
                # just ignore the error - this is a nice to have feature and should not be blocking
                pass
        for rec in self:
            values={
                "partner_id":self.partner_id.id,
                "order_date":self.invoice_date,
                "partner_invoice_id":self.partner_id.id,
                "partner_shipping_id":self.partner_id.id,
                "laundry_person":logged_in_user.id
            }
            _logger.error(values)
            laundry_order = request.env['laundry.order'].sudo().create(values)
        for line_id in self.invoice_line_ids:
            laundry_lines={
                'product_id':line_id.product_id.id,
                'amount':line_id.price_unit,
                'laundry_obj':laundry_order.id,
                'description':line_id.name,
                'qty':line_id.quantity
                }
            _logger.error(laundry_order)
            order_lines = request.env['laundry.order.line'].sudo().create(laundry_lines)
            _logger.error(laundry_order)
            _logger.error('THE ORDER!!!!')
        return {res,laundry_order}