from odoo import api, fields, models, Command, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Description'

    def create(self,vals_list):
        _logger.error('TESTOING')
        # if any('state' in vals and vals.get('state') == 'posted' for vals in vals_list):
        #     raise UserError(_('You cannot create a move already in the posted state. Please create a draft move and post it after.'))
        # vals_list = self._move_autocomplete_invoice_lines_create(vals_list)
        # rec=super(AccountMove, self).create(self,vals_list)
        # for move_id in rec:
        #     _logger.error(move_id.id)
        #     _logger.error('TESTING THE VALUES HERE!!!')
        # return super(AccountMove, self).create(vals_list)s

# class AccountMove(models.Model):
#     _inherit = 'account.move'
#     _description = 'Description'

#     def create(self,vals_list):
#         _logger.error('TESTOING')
#         if any('state' in vals and vals.get('state') == 'posted' for vals in vals_list):
#             raise UserError(_('You cannot create a move already in the posted state. Please create a draft move and post it after.'))
#         vals_list = self._move_autocomplete_invoice_lines_create(vals_list)
#         rec=super(AccountMove, self).create(vals_list)
#         for move_id in rec:
#             _logger.error(move_id.id)
#             _logger.error('TESTING THE VALUES HERE!!!')
        # return super(AccountMove, self).create(vals_list)s