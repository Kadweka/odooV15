# -*- coding: utf-8 -*-

from odoo import api, models


class MultiReportPartnerLedger(models.AbstractModel):
    _name = 'report.multi_currency_partner_ledger_app.report_partnerledger'
    _description = 'multicurrency ledger'

    def _lines(self, data, partner, currency):
        domain = [('move_id.partner_id', '=', partner.id),
                  ('move_id.currency_id', '=', currency.id)]
        move_state = data['move_state']
        if move_state == ['posted']:
            domain += [('move_id.state', '=', 'posted')]
        else:
            domain += [('move_id.state', 'in', ['draft', 'posted'])]

        account_type = data['account_type']
        if account_type == ['supplier']:
            domain += [('account_id.internal_type', '=', 'payable')]
        elif account_type == ['customer']:
            domain += [('account_id.internal_type', '=', 'receivable')]
        else:
            domain += [('account_id.internal_type',
                        'in', ['receivable', 'payable'])]

        if data['date_from'] and not data['date_to']:
            domain += [('date', '>=', data['date_from'])]
        elif data['date_to'] and not data['date_from']:
            domain += [('date', '<=', data['date_to'])]
        elif data['date_from'] and data['date_to']:
            domain += [('date', '>=', data['date_from']),
                       ('date', '<=', data['date_to'])]
        else:
            domain += []
        invoice_ids = self.env['account.move.line'].search(domain)
        full_account = []
        running_balance = 0

        for invoice in invoice_ids:
            company_id = self.env.user.company_id
            displayed_name = str(invoice.move_id.name or '') + \
                '-' + str(invoice.move_id.ref or '')
            debit_amt_convert = invoice.debit
            credit_amt_convert = invoice.credit
            amount_currency_amt_convert = invoice.amount_currency
            balance_amt_convert = invoice.balance
            if company_id.currency_id != invoice.currency_id:
                debit_amt_convert = company_id.currency_id._convert(
                    invoice.debit, invoice.currency_id, company_id, invoice.move_id.date)
                credit_amt_convert = company_id.currency_id._convert(
                    invoice.credit, invoice.currency_id, company_id, invoice.move_id.date)
                amount_currency_amt_convert = invoice.currency_id._convert(
                    invoice.amount_currency, company_id.currency_id, company_id, invoice.move_id.date)
                balance_amt_convert = company_id.currency_id._convert(
                    invoice.balance, invoice.currency_id, company_id, invoice.move_id.date)

            running_balance += abs(debit_amt_convert) - abs(credit_amt_convert)
            vals = {
                'debit': debit_amt_convert,
                'credit': credit_amt_convert,
                'amount_currency': amount_currency_amt_convert,
                'progress': balance_amt_convert,
                'date': invoice.move_id.invoice_date.strftime('%d/%m/%Y') if invoice.move_id.invoice_date else False or invoice.payment_id.payment_date.strftime('%d/%m/%Y') if invoice.payment_id.payment_date else False,
                'date_due': invoice.move_id.invoice_date_due.strftime('%d/%m/%Y') if invoice.move_id.invoice_date_due else False,
                'code': invoice.journal_id.code,
                'a_code': invoice.account_id.code,
                'displayed_name': displayed_name,
                # 'currency_id': invoice.currency_id.symbol or company_id.currency_id.symbol,
                'item_description': invoice.name,
                'currency_id': invoice.currency_id.symbol,
                'invoice_id': invoice.move_id.id,
                'running_balance': running_balance,
            }
            full_account.append(vals)
        running_balance = 0
        return full_account

    def _sum_partner(self, data, partner, currencys):
        total_credit = 0.0
        total_debit = 0.0
        total_balance = 0.0
        total_amount_lst = []
        for currency in currencys:
            records = self._lines(data, partner, currency)
            for record in records:
                total_credit += record['credit']
                total_debit += record['debit']
                total_balance += record['progress']
        total_amount_lst.append({'total_credit': total_credit,
                                 'total_debit': total_debit,
                                 'total_balance': total_balance})
        return total_amount_lst

    @api.model
    def _get_report_values(self, docids, data=None):
        context = data.get('context')
        currency_ids = self.env['res.currency'].browse(
            context.get('currency_ids'))
        partner_ids = self.env['res.partner'].browse(data.get('docs'))
        return {
            'currency_ids': currency_ids,
            'doc_model': self.env['res.partner'],
            'docs': partner_ids,
            'lines': self._lines,
            'extra': data,
            'company_id': self.env.company,
            'sum_partner': self._sum_partner,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
