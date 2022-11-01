# -*- coding:utf-8 -*-

from dataclasses import field
from email.policy import default
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError,MissingError

import logging

_logger = logging.getLogger(__name__)


class HrExpenseReport(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """
    _inherit = 'hr.expense.sheet'
    _description = 'Expense Report'

    reason=fields.Char(string="Reason For Rejection")
    state = fields.Selection([
        ('waiting', 'Submited'),
        ('draft', 'Need Validation'),
        ('submit', 'Need Approval'),
        ('approve', 'Approved'),
        ('post', 'Posted'),
        ('done', 'Done'),
        ('cancel', 'Refused'),
        ], string='State')
    @api.model
    def create(self, vals):
        if vals:
            vals['state']="waiting"
        result = super().create(vals)
        for res in result:
            res.notify_first_approver()
        return result

    def notify_first_approver(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        approver_group = self.env.ref('general_approvers.first_expense_approver')
        users = approver_group.users
        for res in users:
            mail_obj = self.env['mail.mail']
            state = dict(self._fields['state'].selection).get(self.state)
            subject = f"Memo Submition Request For {self.employee_id.name}"
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.private.url')
            email_to = res.login
            body_html = f"""
                <html>
                <body>
                <div style="margin:0px;padding: 0px;">
                    <p style="padding: 0px; font-size: 13px;">
                        Dear {res.name},
                        <br/>
                        You Have Been Requested to Submit Memo  on {self.name} for Validation
                        <br/>
                        .
                        <br/>

                    </p>
                    <p style="margin:16px 0px 16px 0px;">
            <a href="{base_url}/web#id={self.id}&menu_id=193&active_id=12&model=hr.expense.sheet&view_type=form" target="_blank" style="background-color:#875A7B;padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;">
            Confirm Memo
            </a>
        </p>
                <br/>
                </div>
                </body>
                </html>
            """
            mail = mail_obj.sudo().create({
                'body_html': body_html,
                'subject': subject,
                'email_to': email_to
            })
            mail.send()
            return mail

    def need_second_approver(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        if user:
            self.state ='draft'
            self.notify_second_approver()
    def notify_second_approver(self):
        approver_group = self.env.ref('general_approvers.second_expense_approver')
        users = approver_group.users
        for res in users:
            mail_obj = self.env['mail.mail']
            state = dict(self._fields['state'].selection).get(self.state)
            subject = f"Memo Validation Request For {self.employee_id.name}"
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.private.url')
            email_to = res.login
            body_html = f"""
                <html>
                <body>
                <div style="margin:0px;padding: 0px;">
                    <p style="padding: 0px; font-size: 13px;">
                        Dear {res.name},
                        <br/>
                        You Have Been Requested to Validate Memo on {self.name} For it to Be Approved
                        <br/>
                        .
                        <br/>
                    </p>
                    <p style="margin:16px 0px 16px 0px;">
            <a href="{base_url}/web#id={self.id}&menu_id=193&active_id=12&model=hr.expense.sheet&view_type=form" target="_blank" style="background-color:#875A7B;padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;">
            Approve Memo
            </a>
        </p>
                <br/>
                </div>
                </body>
                </html>
            """
            mail = mail_obj.sudo().create({
            'body_html': body_html,
            'subject': subject,
            'email_to': email_to
            })
            mail.send()
            return mail


    def need_third_approver(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        if user:
            self.action_submit_sheet()
            self.notify_third_approver()
    def notify_third_approver(self):
        approver_group = self.env.ref('general_approvers.third_expense_approver')
        users = approver_group.users
        for res in users:
            mail_obj = self.env['mail.mail']
            state = dict(self._fields['state'].selection).get(self.state)
            subject = f"Memo Approval Request For {self.employee_id.name}"
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.private.url')
            email_to = res.login
            body_html = f"""
                <html>
                <body>
                <div style="margin:0px;padding: 0px;">
                    <p style="padding: 0px; font-size: 13px;">
                        Dear {res.name},
                        <br/>
                        You Have Been Requested to Approve Memo for  {self.name}
                        <br/>
                        .
                        <br/>
                    </p>
                    <p style="margin:16px 0px 16px 0px;">
            <a href="{base_url}/web#id={self.id}&menu_id=193&active_id=12&model=hr.expense.sheet&view_type=form" target="_blank" style="background-color:#875A7B;padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;">
            Approve Memo
            </a>
        </p>
                <br/>
                </div>
                </body>
                </html>
            """
            mail = mail_obj.sudo().create({
            'body_html': body_html,
            'subject': subject,
            'email_to': email_to
            })
            mail.send()
            return mail

    def need_owner(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        if user:
            self.approve_expense_sheets()
            self.notify_owner()
        else:
           raise UserError("Your Dont Have Enough permissions")
    def notify_owner(self):
        mail_obj = self.env['mail.mail']
        subject = f"Memo Has Been Approved"
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.private.url')
        email_to = self.employee_id.work_email
        body_html = f"""
            <html>
            <body>
            <div style="margin:0px;padding: 0px;">
                <p style="padding: 0px; font-size: 13px;">
                    Dear {self.employee_id.work_email},
                    <br/>
                    Your Memo Has Been Approved!.
                    <br/>
                    .
                    <br/>
                </p>
                <p style="margin:16px 0px 16px 0px;">
            <a href="{base_url}/web#id={self.id}&menu_id=193&active_id=12&model=hr.expense.sheet&view_type=form" target="_blank" style="background-color:#875A7B;padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;">
        View Memo
        </a>
    </p>
            <br/>
            </div>
            </body>
            </html>
        """
        mail = mail_obj.sudo().create({
            'body_html': body_html,
            'subject': subject,
            'email_to': email_to
        })
        mail.send()
        return mail
