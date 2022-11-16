from odoo import api, fields, models, Command, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_is_zero, float_round, float_repr, float_compare
from odoo.http import request, Response
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

today= datetime.today().strftime('%Y-%m-%d')
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
            laundry_order = request.env['laundry.order'].sudo().create(values)
        for line_id in self.invoice_line_ids:
            laundry_lines={
                'product_id':line_id.product_id.id,
                'amount':line_id.price_unit,
                'laundry_obj':laundry_order.id,
                'description':line_id.name,
                'qty':line_id.quantity
                }
            order_lines = request.env['laundry.order.line'].sudo().create(laundry_lines)
        return {res,laundry_order}



class PosOrder(models.Model):
    _inherit = 'pos.order'
    _description = 'Description'

    def _generate_pos_order_invoice(self):
        context = self._context
        current_uid = context.get('uid')
        logged_in_user = self.env['res.users'].browse(current_uid)
        moves = self.env['account.move']

        for order in self:
            # Force company for all SUPERUSER_ID action
            if order.account_move:
                moves += order.account_move
                continue

            if not order.partner_id:
                raise UserError(_('Please provide a partner for the sale.'))

            move_vals = order._prepare_invoice_vals()
            new_move = order._create_invoice(move_vals)
            laundry_vals = order._prepare_invoice_vals()

            order.write({'account_move': new_move.id, 'state': 'invoiced'})
            new_move.sudo().with_company(order.company_id)._post()
            laundry_order = request.env['laundry.order'].sudo().create({
               "partner_id":new_move.partner_id.id,
                "order_date":new_move.invoice_date,
                "partner_invoice_id":new_move.partner_id.id,
                "partner_shipping_id":new_move.partner_id.id,
                "laundry_person":logged_in_user.id  
            })
            for line_id in new_move.invoice_line_ids:
                    laundry_lines={
                        'product_id':line_id.product_id.id,
                        'amount':line_id.price_unit,
                        'laundry_obj':laundry_order.id,
                        'description':line_id.name,
                        'qty':line_id.quantity
                        }
                    order_lines = request.env['laundry.order.line'].sudo().create(laundry_lines)
            moves += new_move
            order._apply_invoice_payments()

        if not moves:
            return {}

        return {
            'name': _('Customer Invoice'),
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_model': 'account.move',
            'context': "{'move_type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': moves and moves.ids[0] or False,
        }
